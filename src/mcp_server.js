import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import puppeteer from "puppeteer";

// --- GLOBAL STATE ---
let browser;
let page;

// --- SERVER SETUP ---
const server = new Server(
  {
    name: "puppeteer-mcp-server",
    version: "1.0.0",
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
      {
        name: "connect_browser",
        description: "Connect to the existing Chrome instance via remote debugging port 9222",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "navigate",
        description: "Navigate to a URL",
        inputSchema: {
          type: "object",
          properties: { url: { type: "string" } },
          required: ["url"],
        },
      },
      {
        name: "click",
        description: "Click an element by selector",
        inputSchema: {
          type: "object",
          properties: { selector: { type: "string" } },
          required: ["selector"],
        },
      },
      {
        name: "type_text",
        description: "Type text into an element by selector",
        inputSchema: {
          type: "object",
          properties: { selector: { type: "string" }, text: { type: "string" } },
          required: ["selector", "text"],
        },
      },
      {
        name: "upload_file",
        description: "Upload a file to an input[type=file] element",
        inputSchema: {
          type: "object",
          properties: { selector: { type: "string" }, filePath: { type: "string" } },
          required: ["selector", "filePath"],
        },
      },
      {
        name: "get_dom_snapshot",
        description: "Get a simplified snapshot of the current page DOM to find selectors",
        inputSchema: { type: "object", properties: {} },
      }
    ],
  };
});

// --- TOOL EXECUTION ---
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    if (!browser && request.params.name !== "connect_browser") {
      await connectToBrowser();
    }

    switch (request.params.name) {
      case "connect_browser": {
        await connectToBrowser();
        return { content: [{ type: "text", text: "Connected to Chrome on port 9222" }] };
      }

      case "navigate": {
        const { url } = request.params.arguments;
        await page.goto(url);
        return { content: [{ type: "text", text: `Navigated to ${url}` }] };
      }

      case "click": {
        const { selector } = request.params.arguments;
        await page.waitForSelector(selector, { timeout: 5000 });
        await page.click(selector);
        return { content: [{ type: "text", text: `Clicked ${selector}` }] };
      }

      case "type_text": {
        const { selector, text } = request.params.arguments;
        await page.waitForSelector(selector, { timeout: 5000 });
        // Clear input first just in case
        await page.evaluate((sel) => { document.querySelector(sel).value = ''; }, selector);
        await page.type(selector, text);
        return { content: [{ type: "text", text: `Typed into ${selector}` }] };
      }

      case "upload_file": {
        const { selector, filePath } = request.params.arguments;
        const input = await page.$(selector);
        await input.uploadFile(filePath);
        return { content: [{ type: "text", text: `Uploaded ${filePath} to ${selector}` }] };
      }

      case "get_dom_snapshot": {
        const snapshot = await page.evaluate(() => {
            // Helper to get meaningful info
            const getInfo = (el) => {
                let info = `<${el.tagName.toLowerCase()}`;
                if (el.id) info += ` id="${el.id}"`;
                if (el.name) info += ` name="${el.name}"`;
                if (el.className) info += ` class="${el.className}"`;
                if (el.placeholder) info += ` placeholder="${el.placeholder}"`;
                if (el.type) info += ` type="${el.type}"`;
                
                let text = el.innerText ? el.innerText.trim().substring(0, 50) : '';
                // Check for label
                if (el.id) {
                    const label = document.querySelector(`label[for="${el.id}"]`);
                    if (label) text = `[Label: ${label.innerText.trim()}] ` + text;
                }
                
                info += `> ${text}`;
                return info;
            };

            // Focus on interactive elements
            const elements = document.querySelectorAll('input, textarea, button, select, label');
            return Array.from(elements).map(getInfo).join('\n');
        });
        return { content: [{ type: "text", text: snapshot }] };
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
    browser = await puppeteer.connect({
        browserURL: "http://127.0.0.1:9222",
        defaultViewport: null,
    });
    const pages = await browser.pages();
    // Find the application tab
    page = pages.find(p => p.url().includes('career.shiftup.co.kr')) || pages[0];
    await page.bringToFront();
}

// --- START SERVER ---
const transport = new StdioServerTransport();
await server.connect(transport);
