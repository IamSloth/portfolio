import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../');

// --- GLOBAL STATE ---
let browser;
let context;
let page;

// --- SERVER SETUP ---
const server = new Server(
  {
    name: "lim-pipeline-agent",
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
        name: "get_candidate_profile",
        description: "Get the full profile (experience, skills, contact) of Lim Jong Kwon",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "find_latest_resume",
        description: "Find the path to the most recent PDF resume",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "browser_launch",
        description: "Launch a visible browser for automation",
        inputSchema: { type: "object", properties: { headless: { type: "boolean" } } },
      },
      {
        name: "browser_navigate",
        description: "Navigate to a URL",
        inputSchema: { 
            type: "object", 
            properties: { url: { type: "string" } },
            required: ["url"] 
        },
      },
      {
        name: "browser_analyze",
        description: "Analyze the current page for input fields",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "browser_fill",
        description: "Fill a form field or click an element",
        inputSchema: {
          type: "object",
          properties: { 
            selector: { type: "string" }, 
            value: { type: "string" },
            action: { type: "string", enum: ["fill", "click", "upload"] }
          },
          required: ["selector", "action"]
        },
      }
    ],
  };
});

// --- TOOL EXECUTION ---
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    switch (request.params.name) {
      case "get_candidate_profile": {
        const profilePath = path.join(projectRoot, 'config/profile.json');
        if (!fs.existsSync(profilePath)) throw new Error("Profile not found");
        const data = fs.readFileSync(profilePath, 'utf-8');
        return { content: [{ type: "text", text: data }] };
      }

      case "find_latest_resume": {
        const outputDir = path.join(projectRoot, 'output');
        const submittedDir = path.join(projectRoot, 'companies/_submitted');
        // Search logic... (simplified for now)
        return { content: [{ type: "text", text: `Check ${outputDir} or ${submittedDir}` }] };
      }

      case "browser_launch": {
        const headless = request.params.arguments?.headless ?? false;
        browser = await chromium.launch({ headless: headless, args: ['--start-maximized'] });
        context = await browser.newContext({ viewport: null });
        page = await context.newPage();
        return { content: [{ type: "text", text: "Browser Launched" }] };
      }

      case "browser_navigate": {
        const { url } = request.params.arguments;
        if (!page) throw new Error("Browser not started");
        await page.goto(url);
        return { content: [{ type: "text", text: `Navigated to ${url}` }] };
      }

      case "browser_analyze": {
        if (!page) throw new Error("Browser not started");
        const inputs = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('input, textarea, button, select')).map(el => ({
                tag: el.tagName,
                id: el.id,
                name: el.name,
                type: el.type,
                placeholder: el.placeholder,
                visible: el.offsetParent !== null
            }));
        });
        return { content: [{ type: "text", text: JSON.stringify(inputs, null, 2) }] };
      }

      case "browser_fill": {
        const { selector, value, action } = request.params.arguments;
        if (!page) throw new Error("Browser not started");
        
        if (action === 'click') {
            await page.click(selector, { force: true });
            return { content: [{ type: "text", text: `Clicked ${selector}` }] };
        } else if (action === 'upload') {
            await page.locator(selector).setInputFiles(value);
            return { content: [{ type: "text", text: `Uploaded ${value}` }] };
        } else {
            await page.fill(selector, value || '');
            return { content: [{ type: "text", text: `Filled ${selector}` }] };
        }
      }

      default:
        throw new Error(`Unknown tool: ${request.params.name}`);
    }
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Lim-Pipeline MCP Agent Server running on stdio...");