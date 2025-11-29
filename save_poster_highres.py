"""
High-Resolution Poster Export Script
=====================================
Generates a print-ready, high-resolution PNG/PDF of the Load Forecasting poster.

Requirements:
    pip install playwright
    playwright install chromium

Output:
    - poster_highres.png (4x scale, ~3364 x 4756 pixels for A0)
    - poster_print.pdf (A0 size, vector quality)
"""

import asyncio
import os
from pathlib import Path

# Check if playwright is installed
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Installing now...")
    os.system("pip install playwright")
    os.system("playwright install chromium")
    from playwright.async_api import async_playwright


async def save_poster_highres():
    """Generate high-resolution poster image and PDF."""
    
    # Get the path to index.html
    script_dir = Path(__file__).parent
    html_path = script_dir / "index.html"
    output_dir = script_dir / "exports"
    
    # Create exports directory
    output_dir.mkdir(exist_ok=True)
    
    # File URL for the HTML
    file_url = f"file:///{html_path.resolve().as_posix()}"
    
    print("🚀 Starting high-resolution poster export...")
    print(f"📄 Source: {html_path}")
    print(f"📁 Output: {output_dir}")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        
        # === 1. Normal Width PDF (Direct render, no conversion) ===
        print("\n🔹 Generating Normal Width PDF (Direct Render)...")
        
        # First, measure the content
        context_measure = await browser.new_context(viewport={"width": 1200, "height": 800})
        page_measure = await context_measure.new_page()
        await page_measure.goto(file_url, wait_until="networkidle")
        await page_measure.wait_for_timeout(2000)
        
        # Apply PDF-specific styles and get exact content dimensions
        dimensions = await page_measure.evaluate("""
            () => {
                // Remove all margins/spacing
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.background = 'white';
                document.documentElement.style.margin = '0';
                document.documentElement.style.padding = '0';
                
                const container = document.querySelector('.poster-container');
                if (container) {
                    container.style.maxWidth = '100%';
                    container.style.width = '100%';
                    container.style.margin = '0';
                    container.style.boxShadow = 'none';
                    container.style.border = 'none';
                }
                
                const rect = container.getBoundingClientRect();
                return {
                    width: Math.ceil(rect.width),
                    height: Math.ceil(rect.height)
                };
            }
        """)
        print(f"📏 Content dimensions: {dimensions['width']}px x {dimensions['height']}px")
        await context_measure.close()
        
        # Now create PDF with exact dimensions
        # Use scale to fit content perfectly
        content_width = dimensions['width']
        content_height = dimensions['height']
        
        # Create context with exact content size
        context_pdf = await browser.new_context(
            viewport={"width": content_width, "height": content_height},
            device_scale_factor=2  # Good quality for PDF
        )
        page_pdf = await context_pdf.new_page()
        await page_pdf.goto(file_url, wait_until="networkidle")
        await page_pdf.wait_for_timeout(2000)
        
        # Apply fixes
        await page_pdf.evaluate("""
            () => {
                const progressBar = document.getElementById('progressBar');
                if (progressBar) progressBar.style.width = '99.48%';
                const bar1 = document.getElementById('bar1');
                const bar2 = document.getElementById('bar2');
                const bar3 = document.getElementById('bar3');
                if (bar1) bar1.style.height = '140px';
                if (bar2) bar2.style.height = '31px';
                if (bar3) bar3.style.height = '14px';
                document.querySelectorAll('.animate-bounce-slow, .animate-pulse-glow').forEach(el => {
                    el.style.animation = 'none';
                });
                const modal = document.getElementById('imageModal');
                if (modal) modal.style.display = 'none';
                
                // Remove ALL margins/padding/backgrounds that cause white space
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.background = 'white';
                document.documentElement.style.margin = '0';
                document.documentElement.style.padding = '0';
                document.documentElement.style.background = 'white';
                
                // Make poster container full width with no margins
                const container = document.querySelector('.poster-container');
                if (container) {
                    container.style.maxWidth = '100%';
                    container.style.width = '100%';
                    container.style.margin = '0';
                    container.style.padding = '0';
                    container.style.boxShadow = 'none';
                    container.style.border = 'none';
                    container.style.borderRadius = '0';
                }
            }
        """)
        await page_pdf.wait_for_timeout(500)
        
        # Generate PDF with exact fit - no page breaks
        pdf_path_normal = output_dir / "poster_single_page.pdf"
        print("📄 Generating single-page PDF...")
        
        # Calculate scale to fit on standard paper or use custom size
        # Using the exact content size as page size = guaranteed single page
        await page_pdf.pdf(
            path=str(pdf_path_normal),
            width=f"{content_width}px",
            height=f"{content_height}px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=False,
            scale=1
        )
        print(f"✅ Saved: {pdf_path_normal}")
        
        # Also save PNG
        png_path = output_dir / "poster_highres.png"
        await page_pdf.screenshot(path=str(png_path), type="png", full_page=True)
        print(f"✅ Saved PNG: {png_path}")
        
        await context_pdf.close()
        
        # === 2. Wide Version ===
        print("\n🔹 Generating Wide Width PDF (Direct Render)...")
        
        # Measure wide version
        context_wide_measure = await browser.new_context(viewport={"width": 2000, "height": 800})
        page_wide_measure = await context_wide_measure.new_page()
        await page_wide_measure.goto(file_url, wait_until="networkidle")
        await page_wide_measure.wait_for_timeout(2000)
        
        dimensions_wide = await page_wide_measure.evaluate("""
            () => {
                const container = document.querySelector('.poster-container');
                const rect = container.getBoundingClientRect();
                return {
                    width: Math.ceil(rect.width),
                    height: Math.ceil(rect.height)
                };
            }
        """)
        print(f"📏 Wide dimensions: {dimensions_wide['width']}px x {dimensions_wide['height']}px")
        await context_wide_measure.close()
        
        wide_width = dimensions_wide['width']
        wide_height = dimensions_wide['height']
        
        context_wide = await browser.new_context(
            viewport={"width": wide_width, "height": wide_height},
            device_scale_factor=2
        )
        page_wide = await context_wide.new_page()
        await page_wide.goto(file_url, wait_until="networkidle")
        await page_wide.wait_for_timeout(2000)
        
        # Apply fixes
        await page_wide.evaluate("""
            () => {
                const progressBar = document.getElementById('progressBar');
                if (progressBar) progressBar.style.width = '99.48%';
                const bar1 = document.getElementById('bar1');
                const bar2 = document.getElementById('bar2');
                const bar3 = document.getElementById('bar3');
                if (bar1) bar1.style.height = '140px';
                if (bar2) bar2.style.height = '31px';
                if (bar3) bar3.style.height = '14px';
                document.querySelectorAll('.animate-bounce-slow, .animate-pulse-glow').forEach(el => {
                    el.style.animation = 'none';
                });
                const modal = document.getElementById('imageModal');
                if (modal) modal.style.display = 'none';
                
                // Remove ALL margins/padding/backgrounds that cause white space
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.background = 'white';
                document.documentElement.style.margin = '0';
                document.documentElement.style.padding = '0';
                document.documentElement.style.background = 'white';
                
                // Make poster container full width with no margins
                const container = document.querySelector('.poster-container');
                if (container) {
                    container.style.maxWidth = '100%';
                    container.style.width = '100%';
                    container.style.margin = '0';
                    container.style.padding = '0';
                    container.style.boxShadow = 'none';
                    container.style.border = 'none';
                    container.style.borderRadius = '0';
                }
            }
        """)
        await page_wide.wait_for_timeout(500)
        
        pdf_path_wide = output_dir / "poster_wide_single_page.pdf"
        await page_wide.pdf(
            path=str(pdf_path_wide),
            width=f"{wide_width}px",
            height=f"{wide_height}px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=False,
            scale=1
        )
        print(f"✅ Saved: {pdf_path_wide}")
        
        png_wide_path = output_dir / "poster_wide_highres.png"
        await page_wide.screenshot(path=str(png_wide_path), type="png", full_page=True)
        print(f"✅ Saved PNG: {png_wide_path}")
        
        await context_wide.close()
        await browser.close()
    
    print("\n" + "="*50)
    print("🎉 Export Complete!")
    print("="*50)
    print(f"\n📁 Files saved to: {output_dir.resolve()}")
    print("\n📋 Generated files:")
    print(f"   1. poster_highres_8x.png       - Normal width (8x scale)")
    print(f"   2. poster_print_normal.pdf     - Normal PDF")
    print(f"   3. poster_highres_wide_8x.png  - Wide width (8x scale)")
    print(f"   4. poster_print_wide.pdf       - Wide PDF")


if __name__ == "__main__":
    asyncio.run(save_poster_highres())
