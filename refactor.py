import re

def refactor():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Extract CSS
    css_match = re.search(r'<style>([\s\S]*?)</style>', content)
    if css_match:
        css_content = css_match.group(1).strip()
        with open("main.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        content = content.replace(css_match.group(0), '<link rel="stylesheet" href="main.css">')

    # 2. Extract JS (only the inline one, ignoring tamachan-data.js)
    js_match = re.search(r'<script>([\s\S]*?)</script>', content)
    if js_match:
        js_content = js_match.group(1).strip()
        
        # Modify JS to include preventClick on drag-slider
        # We find the drag-slider logic and add link disable code.
        js_content = js_content.replace(
            "const images = slider.querySelectorAll('img');",
            "const images = slider.querySelectorAll('img');\n            const links = slider.querySelectorAll('a');\n            let isDragging = false;\n            slider.addEventListener('mousemove', () => { if(isDown) isDragging = true; });\n            slider.addEventListener('mouseup', () => { setTimeout(() => isDragging = false, 50); });\n            links.forEach(link => { link.addEventListener('click', (e) => { if(isDragging) e.preventDefault(); }); });"
        )
        
        # Expand chat memory 6 -> 20
        js_content = js_content.replace(
            "if (chatHistory.length > 6) chatHistory.shift();",
            "if (chatHistory.length > 20) chatHistory.shift();"
        )
        
        with open("main.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        content = content.replace(js_match.group(0), '<script src="main.js"></script>')
        
    # 3. Fix scrolling="yes" in iframe
    content = content.replace('scrolling="yes"', '')
    
    # 4. Fix aria-labels
    content = content.replace(
        '<button class="chat-close" id="chat-close">',
        '<button class="chat-close" id="chat-close" aria-label="チャットを閉じる">'
    )
    content = content.replace(
        '<button id="chat-send" class="chat-send" onclick="sendChat()">',
        '<button id="chat-send" class="chat-send" aria-label="メッセージを送信" onclick="sendChat()">'
    )
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Refactoring completed successfully: main.css and main.js generated, index.html updated.")

if __name__ == "__main__":
    refactor()
