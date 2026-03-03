import markdown
import os
from frontmatter import Frontmatter
from ebooklib import epub

# Simple script to bundle your 3 recipes into a mobile-ready EPUB
def generate_ggb_bundle():
    book = epub.EpubBook()
    book.set_identifier('ggb-starter-001')
    book.set_title('GGB Starter: 3 Meals, 6 Days')
    book.set_language('en')
    book.add_author('GGB Kitchen')

    recipe_dir = './recipes/en/'
    spine = ['nav']

    # 1. Add Intro Page
    intro_path = './plans/ggb-starter-week/GGB-starter-week.md'
    intro_post = Frontmatter.read_file(intro_path)
    intro_attrs = intro_post['attributes']
    intro_html = epub.EpubHtml(
        title=intro_attrs.get('title', 'Introduction'),
        file_name='intro.xhtml',
        content=markdown.markdown(intro_post['body'])
    )
    book.add_item(intro_html)
    spine.append(intro_html)

    # 2. Add Recipes
    for filename in sorted(os.listdir(recipe_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(recipe_dir, filename)
            post = Frontmatter.read_file(filepath)
            attrs = post['attributes']
            html_content = markdown.markdown(post['body'])

            title = attrs.get('title', filename[:-3])
            slug = attrs.get('slug', filename[:-3])

            # Combine metadata and content for the page
            full_html = f"<h1>{title}</h1>"
            if 'prep_time' in attrs and 'cook_time' in attrs:
                full_html += f"<ul><li>Prep: {attrs['prep_time']}</li><li>Cook: {attrs['cook_time']}</li></ul>"
            if 'ingredients' in attrs:
                full_html += "<h3>Ingredients</h3><ul>"
                for ing in attrs['ingredients']:
                    full_html += f"<li>{ing}</li>"
                full_html += "</ul>"
            full_html += html_content

            item = epub.EpubHtml(title=title, file_name=f"{slug}.xhtml", content=full_html)
            book.add_item(item)
            spine.append(item)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    epub.write_epub('GGB_Starter_Plan.epub', book)
    print("Bundle Generated: GGB_Starter_Plan.epub")

if __name__ == "__main__":
    generate_ggb_bundle()