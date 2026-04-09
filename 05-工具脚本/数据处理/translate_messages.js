const XLSX = require('xlsx');

// 读取Excel文件
const workbook = XLSX.readFile('推特及领英25年10月至26年03月私信内容.xlsx');

// 处理每个工作表
const sheets = ['x（EN）', 'x（CN） ', '领英'];

sheets.forEach(sheetName => {
  const worksheet = workbook.Sheets[sheetName];
  if (!worksheet) {
    console.log(`工作表 ${sheetName} 不存在`);
    return;
  }
  
  const data = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });
  
  console.log(`\n处理工作表: ${sheetName}`);
  console.log(`总行数: ${data.length}`);
  
  // 找到列索引
  const headers = data[0];
  const userCol = headers.indexOf('用户名');
  const dateCol = headers.indexOf('发送日期');
  const typeCol = headers.indexOf('消息类型');
  const coreCol = headers.indexOf('核心信息');
  const transCol = headers.indexOf('中文翻译');
  const fullCol = headers.indexOf('完整对话');
  
  console.log(`列索引 - 用户名:${userCol}, 核心信息:${coreCol}, 中文翻译:${transCol}, 完整对话:${fullCol}`);
  
  // 处理每一行数据（从第2行开始，跳过表头）
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const username = row[userCol] || '';
    const fullMessage = row[fullCol] || '';
    
    if (!username || !fullMessage) continue;
    
    console.log(`\n第${i}行 - 用户: ${username}`);
    console.log(`原始消息长度: ${fullMessage.length}`);
    
    // 这里需要填充翻译和核心信息
    // 由于无法调用翻译API，我们先标记需要处理的行
    if (!row[coreCol]) {
      row[coreCol] = '[待提炼]';
    }
    if (!row[transCol]) {
      row[transCol] = '[待翻译]';
    }
  }
  
  // 将数据写回工作表
  const newWorksheet = XLSX.utils.aoa_to_sheet(data);
  workbook.Sheets[sheetName] = newWorksheet;
});

// 保存文件
XLSX.writeFile(workbook, '推特及领英25年10月至26年03月私信内容_已处理.xlsx');
console.log('\n处理完成！');
