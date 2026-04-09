// 使用 Chrome DevTools Protocol 滚动 X 私信页面
const CDP = require('chrome-remote-interface');

async function scrollToDate() {
    let client;
    try {
        // 连接到 Chrome
        client = await CDP();
        const {Page, Runtime} = client;
        
        // 启用必要的域
        await Page.enable();
        await Runtime.enable();
        
        // 获取所有标签页
        const targets = await CDP.List();
        const xMessagesTab = targets.find(t => t.url.includes('x.com/messages'));
        
        if (!xMessagesTab) {
            console.log('未找到 X 私信页面，请确保页面已打开');
            return;
        }
        
        console.log('找到 X 私信页面，开始滚动...');
        
        // 连接到特定标签页
        const tabClient = await CDP({target: xMessagesTab.id});
        const {Runtime: TabRuntime} = tabClient;
        await TabRuntime.enable();
        
        // 执行滚动脚本
        const scrollScript = `
            (function() {
                let scrollCount = 0;
                const maxScrolls = 100; // 最多滚动100次
                
                function scrollMessages() {
                    // 尝试多个可能的滚动容器
                    const selectors = [
                        '[data-testid="DMDrawer"]',
                        '[aria-label*="时间线"]',
                        '[role="region"]',
                        'main [style*="overflow"]'
                    ];
                    
                    let container = null;
                    for (const selector of selectors) {
                        container = document.querySelector(selector);
                        if (container) break;
                    }
                    
                    if (!container) {
                        console.log('未找到滚动容器');
                        return;
                    }
                    
                    // 检查是否有日期为 2025年10月1日 的消息
                    const messages = document.querySelectorAll('[data-testid="conversation"]');
                    for (const msg of messages) {
                        const text = msg.textContent;
                        if (text.includes('2025') && (text.includes('10月1') || text.includes('Oct 1'))) {
                            console.log('找到目标日期的消息！');
                            msg.scrollIntoView({behavior: 'smooth', block: 'center'});
                            return;
                        }
                    }
                    
                    // 继续滚动
                    if (scrollCount < maxScrolls) {
                        container.scrollTop += 500;
                        scrollCount++;
                        console.log('滚动次数:', scrollCount);
                        setTimeout(scrollMessages, 800);
                    } else {
                        console.log('已达到最大滚动次数');
                    }
                }
                
                scrollMessages();
            })();
        `;
        
        await TabRuntime.evaluate({expression: scrollScript});
        
        console.log('滚动脚本已执行，请查看浏览器');
        
        // 等待一段时间让滚动完成
        await new Promise(resolve => setTimeout(resolve, 60000));
        
    } catch (err) {
        console.error('错误:', err.message);
        console.log('\n请确保：');
        console.log('1. Chrome 已启动并开启了远程调试');
        console.log('2. 启动命令：/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222');
    } finally {
        if (client) {
            await client.close();
        }
    }
}

scrollToDate();
