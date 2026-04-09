const { chromium } = require('playwright');

async function scrollToDate() {
    console.log('启动浏览器...');
    
    // 连接到已运行的 Chrome 实例
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const contexts = browser.contexts();
    
    if (contexts.length === 0) {
        console.log('未找到浏览器上下文');
        await browser.close();
        return;
    }
    
    const context = contexts[0];
    const pages = context.pages();
    
    // 查找 X 私信页面
    let targetPage = null;
    for (const page of pages) {
        const url = page.url();
        if (url.includes('x.com/messages')) {
            targetPage = page;
            console.log('找到 X 私信页面:', url);
            break;
        }
    }
    
    if (!targetPage) {
        console.log('未找到 X 私信页面，打开新页面...');
        targetPage = await context.newPage();
        await targetPage.goto('https://x.com/messages/requests');
        await targetPage.waitForTimeout(3000);
    }
    
    console.log('开始滚动...');
    
    // 执行滚动脚本
    const result = await targetPage.evaluate(async () => {
        // 查找滚动容器 - 使用多种方法
        let container = null;
        const candidates = [];
        
        // 方法1: 查找所有可能的滚动容器
        document.querySelectorAll('*').forEach(el => {
            const style = window.getComputedStyle(el);
            if ((style.overflowY === 'auto' || style.overflowY === 'scroll' || style.overflow === 'auto' || style.overflow === 'scroll') && 
                el.scrollHeight > el.clientHeight) {
                candidates.push({
                    element: el,
                    tag: el.tagName,
                    id: el.id,
                    className: el.className.substring(0, 50),
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight,
                    overflowY: style.overflowY
                });
            }
        });
        
        console.log('找到', candidates.length, '个可滚动元素');
        candidates.slice(0, 5).forEach((c, i) => {
            console.log(`候选 ${i+1}:`, c.tag, c.className, `高度: ${c.scrollHeight}/${c.clientHeight}`);
        });
        
        // 优先选择最大的可滚动容器
        if (candidates.length > 0) {
            candidates.sort((a, b) => b.scrollHeight - a.scrollHeight);
            container = candidates[0].element;
            console.log('选择最大的容器:', candidates[0].tag, candidates[0].className);
        }
        
        if (!container) {
            console.log('未找到滚动容器，尝试滚动整个窗口');
            // 如果找不到容器，尝试滚动整个窗口
            return { success: false, message: '未找到滚动容器，将尝试滚动窗口' };
        }
        
        console.log('找到滚动容器，开始滚动...', 'scrollTop:', container.scrollTop, 'scrollHeight:', container.scrollHeight);
        
        return new Promise((resolve) => {
            let count = 0;
            const maxScrolls = 200;
            
            function doScroll() {
                const oldTop = container.scrollTop;
                
                // 尝试多种滚动方式
                container.scrollTop += 500;
                container.scrollBy(0, 500);
                
                const newTop = container.scrollTop;
                count++;
                
                console.log(`滚动 #${count}: ${oldTop} -> ${newTop}, 差值: ${newTop - oldTop}`);
                
                // 检查是否有 2025年10月1日
                const text = document.body.innerText;
                if (text.includes('2025') && (text.includes('10月1') || text.includes('Oct 1') || text.includes('10/1'))) {
                    console.log('找到 2025年10月1日 的消息！');
                    resolve({ success: true, message: '找到目标日期', scrollCount: count });
                    return;
                }
                
                // 检查是否到底
                if (newTop === oldTop) {
                    console.log('滚动位置没有变化，已到达底部');
                    resolve({ success: false, message: '已到达底部，未找到目标日期', scrollCount: count });
                    return;
                }
                
                // 继续滚动
                if (count < maxScrolls) {
                    setTimeout(doScroll, 1000);
                } else {
                    console.log('达到最大滚动次数');
                    resolve({ success: false, message: '达到最大滚动次数', scrollCount: count });
                }
            }
            
            doScroll();
        });
    });
    
    console.log('滚动完成，结果:', result);
    
    // 不关闭浏览器，保持页面打开
    // await browser.close();
}

scrollToDate().catch(console.error);
