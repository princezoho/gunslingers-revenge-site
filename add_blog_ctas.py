#!/usr/bin/env python3
"""
Add Newsletter and Steam CTAs to all blog posts
"""

from pathlib import Path

# CTA HTML to add to blog posts
blog_cta_html = """
    <!-- Newsletter CTA for Blog Posts -->
    <section class="newsletter-section" style="margin-top: 3rem;">
        <h2>Want More Deck-Building Tips?</h2>
        <p>Join our newsletter for exclusive strategy guides and development updates!</p>
        <form class="newsletter-form" action="#" method="POST" onsubmit="subscribeFromBlog(event)">
            <input type="email" placeholder="Enter your email" required>
            <button type="submit" class="btn">Subscribe</button>
        </form>
        <p style="margin-top: 1rem; font-size: 0.9rem;">Already subscribed? <a href="https://store.steampowered.com/app/XXXXX/Gunslingers_Revenge/" target="_blank" style="color: #c87f2f; font-weight: bold;">Add to Steam Wishlist →</a></p>
    </section>

    <script>
        function subscribeFromBlog(event) {
            event.preventDefault();
            const email = event.target.querySelector('input[type="email"]').value;
            console.log('Blog newsletter subscription:', email);
            alert('Thank you for subscribing! Check your email for confirmation.');
            // After newsletter signup from blog, encourage Steam wishlist
            setTimeout(() => {
                if (confirm('Great! Now add Gunslinger\\'s Revenge to your Steam wishlist to be notified when we launch!')) {
                    window.open('https://store.steampowered.com/app/XXXXX/Gunslingers_Revenge/', '_blank');
                }
            }, 1000);
        }
    </script>
"""

# Process all blog post files
posts_dir = Path("posts")
for post_file in posts_dir.glob("*.html"):
    print(f"Processing {post_file}...")
    
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert the CTA (before the closing main tag or body tag)
    if '</main>' in content:
        content = content.replace('</main>', blog_cta_html + '\n</main>')
    elif '</article>' in content:
        content = content.replace('</article>', '</article>\n' + blog_cta_html)
    else:
        # Insert before </body>
        content = content.replace('</body>', blog_cta_html + '\n</body>')
    
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Added CTAs to {post_file}")

print("\nBlog CTA addition complete!")