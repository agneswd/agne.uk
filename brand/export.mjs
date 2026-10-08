// Exports the brand PNGs from brand/svg with any Chromium browser (Playwright).
// Usage: bunx --bun playwright-core is not needed; run with Node and playwright-core installed:
//   CDP_URL=http://127.0.0.1:9222 node brand/export.mjs      (an already running Chromium with remote debugging)
//   node brand/export.mjs                                     (launches a local Chromium instead)
// Writes brand/png/*.png. Fonts for the og image and header come from public/fonts.
import { chromium } from "playwright-core";
import { readFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const svg = (name) => readFileSync(join(root, "svg", name), "utf8");
const serif = readFileSync(join(root, "..", "public", "fonts", "InstrumentSerif-Regular.woff2")).toString("base64");
const sized = (s, w, h) => s.replace("<svg ", `<svg width="${w}" height="${h}" `);
const page = (body, bg = "transparent") => `<html><head><style>@font-face{font-family:IS;src:url(data:font/woff2;base64,${serif})}html,body{margin:0;background:${bg};overflow:hidden}</style></head><body>${body}</body></html>`;

// name, width, height, html. The wordmark keeps its own aspect ratio (4122 x 1380).
const jobs = [
  ["icon-dark-1024.png", 1024, 1024, page(sized(svg("icon-dark-square.svg"), 1024, 1024))],
  ["icon-dark-512.png", 512, 512, page(sized(svg("icon-dark-square.svg"), 512, 512))],
  ["icon-dark-192.png", 192, 192, page(sized(svg("icon-dark-square.svg"), 192, 192))],
  ["apple-touch-icon-180.png", 180, 180, page(sized(svg("icon-dark-square.svg"), 180, 180))],
  ["icon-dark-rounded-512.png", 512, 512, page(sized(svg("icon-dark-rounded.svg"), 512, 512))],
  ["icon-light-512.png", 512, 512, page(sized(svg("icon-light-square.svg"), 512, 512))],
  ["avatar-800.png", 800, 800, page(sized(svg("icon-dark-square.svg"), 800, 800))],
  ["wordmark-on-dark-2400.png", 2400, 803, page(sized(svg("wordmark-on-dark.svg"), 2400, 803), "#141311")],
  ["wordmark-on-light-2400.png", 2400, 803, page(sized(svg("wordmark-on-light.svg"), 2400, 803), "#EFE9DD")],
  ["wordmark-transparent-2400.png", 2400, 803, page(sized(svg("wordmark-on-dark.svg"), 2400, 803))],
  ["og-1200x630.png", 1200, 630, page(`<div style="width:1200px;height:630px;display:flex;flex-direction:column;justify-content:center;padding:0 96px;box-sizing:border-box;color:#EFE9DD"><div style="width:620px">${svg("wordmark-on-dark.svg")}</div><div style="font:400 64px/1.05 IS;margin-top:36px">Small, careful software</div></div>`, "#141311")],
  ["play-header-4096x2304.png", 4096, 2304, page(`<div style="width:4096px;height:2304px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#EFE9DD"><div style="width:1900px">${svg("wordmark-on-dark.svg")}</div><div style="font:400 190px/1 IS;margin-top:110px">Small, careful software</div></div>`, "#141311")],
];

mkdirSync(join(root, "png"), { recursive: true });
const browser = process.env.CDP_URL ? await chromium.connectOverCDP(process.env.CDP_URL) : await chromium.launch();
const context = process.env.CDP_URL ? browser.contexts()[0] : await browser.newContext();
for (const [name, w, h, html] of jobs) {
  const p = await context.newPage();
  await p.setViewportSize({ width: w, height: h });
  await p.setContent(html);
  await p.waitForTimeout(400);
  await p.bringToFront();
  await p.screenshot({ path: join(root, "png", name), omitBackground: !html.includes("background:#") || html.includes("background:transparent") });
  await p.close();
  console.log("wrote", name);
}
await browser.close().catch(() => {});
