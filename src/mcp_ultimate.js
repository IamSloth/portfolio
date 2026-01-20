import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { chromium } from 'playwright'; // Use standard playwright
import fs from 'fs/promises';
import path from 'path';

// --- GLOBAL STATE ---
let browser;
let context;
let page;

// --- SERVER SETUP ---
const server = new Server(
  {
    name: "ultimate-pipeline-mcp",
    version: "3.0.0",
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
        name: "launch_browser",
        description: "Launch a new visible browser instance (Playwright)",
        inputSchema: { type: "object", properties: { headless: { type: "boolean" } } },
      },
      {
        name: "connect_existing_chrome",
        description: "Connect to existing Chrome on port 9222",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "goto_url",
        description: "Navigate to a URL",
        inputSchema: { 
            type: "object", 
            properties: { url: { type: "string" } },
            required: ["url"] 
        },
      },
      {
        name: "smart_fill",
        description: "Intelligently fill a form field (Text or File)",
        inputSchema: {
          type: "object",
          properties: { 
            selector: { type: "string" }, 
            value: { type: "string" },
            type: { type: "string", enum: ["text", "file", "click"] }
          },
          required: ["selector", "type"]
        },
      },
      {
        name: "analyze_dom",
        description: "Analyze current page DOM for form fields",
        inputSchema: { type: "object", properties: {} },
      }
    ],
  };
});

// --- TOOL EXECUTION ---
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    switch (request.params.name) {
      case "launch_browser": {
        const headless = request.params.arguments?.headless ?? false;
        browser = await chromium.launch({ headless: headless });
        context = await browser.newContext();
        page = await context.newPage();
        return { content: [{ type: "text", text: "Launched new Playwright browser" }] };
      }

      case "connect_existing_chrome": {
        browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
        context = browser.contexts()[0];
        const pages = context.pages();
        // Find career page or first page
        page = pages.find(p => p.url().includes('career')) || pages[0];
        await page.bringToFront();
        return { content: [{ type: "text", text: `Connected to Chrome. Active page: ${await page.title()}` }] };
      }

      case "goto_url": {
        const { url } = request.params.arguments;
        if (!page) throw new Error("No active page. Connect or launch browser first.");
        await page.goto(url);
        return { content: [{ type: "text", text: `Navigated to ${url}` }] };
      }

      case "analyze_dom": {
        if (!page) throw new Error("No active page.");
        const snapshot = await page.evaluate(() => {
            const inputs = Array.from(document.querySelectorAll('input, textarea, select, button'));
            return inputs.map(el => {
                let label = '';
                if (el.id) {
                    const labelEl = document.querySelector(`label[for="${el.id}"]`);
                    if (labelEl) label = labelEl.innerText.trim();
                }
                return {
                    tag: el.tagName,
                    id: el.id,
                    name: el.name,
                    type: el.type,
                    label: label,
                    placeholder: el.placeholder,
                    isVisible: el.offsetParent !== null
                };
            });
        });
        return { content: [{ type: "text", text: JSON.stringify(snapshot, null, 2) }] };
      }

      case "smart_fill": {
        const { selector, value, type } = request.params.arguments;
        if (!page) throw new Error("No active page.");
        
        // Smart wait
        await page.waitForSelector(selector, { state: 'attached', timeout: 5000 });

        if (type === 'click') {
            await page.click(selector, { force: true }); // Force click for hidden checkboxes
            return { content: [{ type: "text", text: `Clicked ${selector}` }] };
        } 
        else if (type === 'file') {
            const input = await page.locator(selector);
            await input.setInputFiles(value);
            return { content: [{ type: "text", text: `Uploaded ${value} to ${selector}` }] };
        }
        else { // text
            await page.fill(selector, value);
            return { content: [{ type: "text", text: `Filled ${selector} with "${value}"` }] };
        }
      }

      default:
        throw new Error(`Unknown tool: ${request.params.name}`);
    }
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

// --- START SERVER ---
const transport = new StdioServerTransport();
await server.connect(transport);
