// 微信公众号后台文章数据提取脚本
// 使用方法：
// 1. 在公众号后台打开"内容管理" → "图文消息"页面
// 2. 按 F12 打开浏览器开发者工具
// 3. 切换到 Console（控制台）标签
// 4. 复制粘贴下面的代码并按回车运行
// 5. 代码会自动提取文章数据并下载为 JSON 文件

(function() {
  console.log('开始提取文章数据...');
  
  const articles = [];
  
  // 方法1：尝试从表格中提取
  const tableRows = document.querySelectorAll('table tbody tr, .list_table tbody tr');
  console.log(`找到 ${tableRows.length} 行表格数据`);
  
  tableRows.forEach((row, index) => {
    const cells = row.querySelectorAll('td');
    if (cells.length > 0) {
      const rowData = {
        index: index + 1,
        cells: Array.from(cells).map(cell => cell.textContent?.trim() || ''),
        links: Array.from(row.querySelectorAll('a')).map(a => ({
          text: a.textContent?.trim(),
          href: a.getAttribute('href')
        }))
      };
      articles.push(rowData);
    }
  });
  
  // 方法2：如果方法1没找到，尝试其他选择器
  if (articles.length === 0) {
    console.log('尝试其他选择器...');
    
    const items = document.querySelectorAll('[class*="appmsg"], [class*="article"], [class*="msg"]');
    console.log(`找到 ${items.length} 个可能的文章元素`);
    
    items.forEach((item, index) => {
      const texts = [];
      const walker = document.createTreeWalker(
        item,
        NodeFilter.SHOW_TEXT,
        null
      );
      
      let node;
      while (node = walker.nextNode()) {
        const text = node.textContent?.trim();
        if (text && text.length > 0 && text.length < 200) {
          texts.push(text);
        }
      }
      
      if (texts.length > 0) {
        articles.push({
          index: index + 1,
          texts: texts.slice(0, 10), // 只取前10个文本
          className: item.className
        });
      }
    });
  }
  
  // 方法3：提取页面所有可见文本（作为备用）
  if (articles.length === 0) {
    console.log('使用通用方法提取页面内容...');
    
    const allText = document.body.innerText;
    articles.push({
      method: 'fullPageText',
      content: allText.substring(0, 5000) // 前5000字符
    });
  }
  
  console.log(`共提取 ${articles.length} 条数据`);
  console.log('数据预览:', articles.slice(0, 3));
  
  // 下载为 JSON 文件
  const dataStr = JSON.stringify(articles, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `公众号文章数据_${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  
  console.log('数据已下载！');
  
  return articles;
})();
