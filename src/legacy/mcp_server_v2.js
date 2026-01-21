import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import puppeteer from "puppeteer-core";
import fs from 'fs/promises';
import path from 'path';

// --- GLOBAL STATE ---
let browser;
let page;
const ALLOWED_DIRS = [
    path.resolve(process.cwd(), 'assets'),
    path.resolve(process.cwd(), 'config'),
    path.resolve(process.cwd(), 'output')
];

// --- SERVER SETUP ---
const server = new Server(
  {
    name: "lim-pipeline-mcp",
    version: "2.0.0", // Upgraded version
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// --- TOOLS DEFINITION ---
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // --- BROWSER TOOLS ---
      {
        name: "connect_browser",
        description: "Connect to Chrome (port 9222)",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "analyze_page",
        description: "Get comprehensive analysis of current page (DOM, URL, Title)",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "interact_element",
        description: "Click or Type into an element",
        inputSchema: {
          type: "object",
          properties: { 
            action: { type: "string", enum: ["click", "type", "upload"] },
            selector: { type: "string" },
            value: { type: "string" } // Text to type or File path
          },
          required: ["action", "selector"],
        },
      },
      
      // --- FILESYSTEM TOOLS (Simplified for Pipeline) ---
      {
        name: "list_files",
        description: "List files in allowed directories (assets, output)",
        inputSchema: {
          type: "object",
          properties: { dirPath: { type: "string" } },
          required: ["dirPath"],
        },
      },
      {
        name: "read_file_content",
        description: "Read content of a file",
        inputSchema: {
          type: "object",
          properties: { filePath: { type: "string" } },
          required: ["filePath"],
        },
      }
    ],
  };
});

// --- TOOL EXECUTION ---
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Auto-connect if needed
    if (!browser && request.params.name !== "connect_browser" && 
        ["analyze_page", "interact_element"].includes(request.params.name)) {
        await connectToBrowser();
    }

    switch (request.params.name) {
      // --- BROWSER ---
      case "connect_browser":
        await connectToBrowser();
        return { content: [{ type: "text", text: "Connected to Chrome" }] };

      case "analyze_page": {
        const title = await page.title();
        const url = await page.url();
        const dom = await page.evaluate(() => {
             // Smart DOM Walker
             const inputs = Array.from(document.querySelectorAll('input, textarea, button, select'));
             return inputs.map(el => ({
                 tag: el.tagName,
                 id: el.id,
                 name: el.name,
                 type: el.type,
                 placeholder: el.placeholder,
                 visible: el.offsetParent !== null
             }));
        });
        return { content: [{ type: "text", text: JSON.stringify({ title, url, dom }, null, 2) }] };
      }

      case "interact_element": {
        const { action, selector, value } = request.params.arguments;
        
        if (action === 'click') {
            await page.click(selector);
            return { content: [{ type: "text", text: `Clicked ${selector}` }] };
        } else if (action === 'type') {
            await page.type(selector, value);
            return { content: [{ type: "text", text: `Typed "${value}" into ${selector}` }] };
        } else if (action === 'upload') {
            const input = await page.$(selector);
            await input.uploadFile(value);
            return { content: [{ type: "text", text: `Uploaded ${value}` }] };
        }
        break;
      }

      // --- FILESYSTEM ---
      case "list_files": {
        const { dirPath } = request.params.arguments;
        // Security Check
        const fullPath = path.resolve(dirPath);
        if (!ALLOWED_DIRS.some(allowed => fullPath.startsWith(allowed))) {
             throw new Error("Access Denied: Directory not allowed.");
        }
        const files = await fs.readdir(fullPath);
        return { content: [{ type: "text", text: files.join('\n') }] };
      }

      case "read_file_content": {
        const { filePath } = request.params.arguments;
        // Security Check
        const fullPath = path.resolve(filePath);
        if (!ALLOWED_DIRS.some(allowed => fullPath.startsWith(allowed))) {
             throw new Error("Access Denied: File not allowed.");
        }
        const content = await fs.readFile(fullPath, 'utf-8');
        return { content: [{ type: "text", text: content }] };
      }

      default:
        throw new Error("Unknown tool");
    }
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

async function connectToBrowser() {
    if (browser) return;
    try {
        browser = await puppeteer.connect({
            browserURL: "http://127.0.0.1:9222",
            defaultViewport: null,
        });
        const pages = await browser.pages();
        // Find career page or fallback to first
        page = pages.find(p => p.url().includes('career')) || pages[0];
        await page.bringToFront();
    } catch (e) {
        throw new Error("Failed to connect to Chrome. Is it running with remote-debugging-port=9222?");
    }
}

// --- START SERVER ---
const transport = new StdioServerTransport();
await server.connect(transport);
