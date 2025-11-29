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
        
        # === 1. Normal Width (Ultra High Res - 8x) ===
        print("\n🔹 Generating Normal Width Version (8x Scale)...")
        context_normal = await browser.new_context(
            viewport={"width": 1200, "height": 1600},
            device_scale_factor=8  # 8x resolution as requested
        )
        page_normal = await context_normal.new_page()
        await page_normal.goto(file_url, wait_until="networkidle")
        await page_normal.wait_for_timeout(2000)
        
        # Apply fixes to normal page
        await page_normal.evaluate("""
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
            }
        """)
        await page_normal.wait_for_timeout(500)
        
        poster_normal = await page_normal.query_selector(".poster-container")
        if poster_normal:
            png_path_normal = output_dir / "poster_highres_8x.png"
            print("📸 Capturing 8x PNG...")
            await poster_normal.screenshot(path=str(png_path_normal), type="png")
            print(f"✅ Saved: {png_path_normal}")
            
            # PDF for normal
            pdf_path_normal = output_dir / "poster_print_normal.pdf"
            await page_normal.pdf(path=str(pdf_path_normal), format="A0", print_background=True)
            print(f"✅ Saved PDF: {pdf_path_normal}")

        await context_normal.close()

        # === 2. Wide Width (Ultra High Res - 8x) ===
        print("\n🔹 Generating Wide Width Version (8x Scale)...")
        # Base width 2000px for wider layout
        context_wide = await browser.new_context(
            viewport={"width": 2000, "height": 2500},
            device_scale_factor=8  # 8x resolution
        )
        page_wide = await context_wide.new_page()
        await page_wide.goto(file_url, wait_until="networkidle")
        await page_wide.wait_for_timeout(2000)
        
        # Apply fixes to wide page
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
            }
        """)
        await page_wide.wait_for_timeout(500)
        
        poster_wide = await page_wide.query_selector(".poster-container")
        if poster_wide:
            png_path_wide = output_dir / "poster_highres_wide_8x.png"
            print("📸 Capturing Wide 8x PNG...")
            await poster_wide.screenshot(path=str(png_path_wide), type="png")
            print(f"✅ Saved: {png_path_wide}")
            
            # PDF for wide (using custom size)
            pdf_path_wide = output_dir / "poster_print_wide.pdf"
            # Calculate height based on aspect ratio or use viewport height
            # Viewport is 2000x2500, so we use that
            await page_wide.pdf(path=str(pdf_path_wide), width="2000px", height="2500px", print_background=True)
            print(f"✅ Saved PDF: {pdf_path_wide}")

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
