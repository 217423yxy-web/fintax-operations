const XLSX = require('xlsx');

// 翻译和核心信息数据
const translations = {
  'x（EN）': [
    {
      user: 'GTM Labs',
      core: '寻求建立合作伙伴关系，提议推荐、收益分享和跨客户协作',
      trans: '你好FinTax，我是GTM Labs的。我们正在扩展可信合作伙伴生态系统，用于推荐、收益分享和跨客户协作——特别是与Web3增长、上市和开发领域的团队合作。我相信我们之间可能有很强的协同效应，并有可能建立真正的双赢结构。愿意快速讨论一下探索这个机会吗？嘿，如果infofi的东西现在不太相关，没关系。你现在实际上对什么话题感兴趣？我们的研究团队总是愿意深入研究对你们真正相关的任何内容。'
    },
    {
      user: 'Laura Rosales',
      core: '询问是否曾经见过面',
      trans: '嘿，不知道为什么，但我有种感觉我们以前见过？！哈哈，我们见过吗？'
    },
    {
      user: 'ESTEEMED',
      core: '分享infofi倒闭分析报告，推广Web3营销策略，邀请通话讨论2026年扩展计划',
      trans: '嘿 @FinTax_Official，我们团队分析了infofi的倒闭以及它对Web3营销策略的意义。产品驱动增长重新成为主流：https://x.com/surgence_io/status/2012871184715837478 如果你想在2026年扩展规模，请告诉我，很想跳上电话聊聊。'
    },
    {
      user: 'Chloee',
      core: '询问是否在线',
      trans: '你现在有机会在线吗😩'
    },
    {
      user: 'Chloee',
      core: '询问对方是否擅长发短信还是只擅长刷推特',
      trans: '你真的擅长发短信还是只擅长刷推特😂',
      date: '2026-02-03'
    },
    {
      user: 'MORGS',
      core: '推广设计订阅服务，提供产品视觉、动效、改版、演示文稿、落地页和营销资产',
      trans: '嘿团队！！我通过生态系统地图看到了你们的资料，想联系一下。我运营MORGS，一个设计订阅服务，帮助团队快速完成产品视觉、动效、改版、演示文稿、落地页和营销资产，无需代理机构的拖延。如果有用，很乐意分享一些例子，看看我们做的任何事情是否能支持你们正在构建的东西。快速关注这里。我们作为一个始终在线的设计订阅运营，按请求优先级排序，快速交付。涵盖持续资产和更大的项目。如果有用，很乐意联系！'
    },
    {
      user: 'Jay Franks',
      core: 'Consensus VC Fund招聘远程工作人员，并提供5-10万美元项目投资机会',
      trans: '你好！这是Consensus VC Fund @consensusvcfund 的团队。我们公司是一家风险投资公司，我们想邀请你以远程方式加入我们的团队，享有固定薪酬、灵活的工作时间和强大友好的团队！此外，如果你正在做一个寻求资金的项目，可以告诉我们。你只需要提交一份表格，批准后可以获得5万到10万美元甚至更多的投资。我们很乐意详细讨论潜在的合作。由于X更新了，我们不总能快速看到回复。如果你使用iOS，可以从App Store下载应用：Sonance: Calls，然后与我们通话，这样我们可以实时交谈。会议室：Wintrack | 我们几乎24/7在Sonance在线，所以你可以随时加入通话。只需在应用中发送通话请求。'
    },
    {
      user: 'Lucy',
      core: '询问是否在线',
      trans: '你现在有机会在线吗'
    },
    {
      user: 'Chloee',
      core: '询问对方是否擅长发短信还是只擅长刷推特',
      trans: '你真的擅长发短信还是只擅长刷推特😂'
    },
    {
      user: 'Molly Clarkk',
      core: '询问想先听好消息还是坏消息',
      trans: '嗨，你想先听好消息还是先听坏消息？？'
    },
    {
      user: 'Nicholas Saunders',
      core: '表达多年来承受工作压力和孤独的感受',
      trans: '多年来，我一直承受着工作的重压，生活在孤独中——世界压在我身上，抑郁...'
    },
    {
      user: 'Gizmolab',
      core: '新广告专员自我介绍',
      trans: '你好！我想自我介绍一下。我是你在X上账号的新广告专员。关于税务...'
    },
    {
      user: '@GoGalaGames',
      core: '提供工程支持服务，曾与GoGalaGames等项目合作',
      trans: '嘿，我们为新兴和快速增长的项目提供工程支持，曾与@GoGalaGames合作...'
    },
    {
      user: 'Aakash Jaggi',
      core: '声称是最亲密的朋友，明天将被带走',
      trans: 'William Hayes，我是Isabella Collins。你是我最亲密的朋友，明天我就要被带走了...'
    },
    {
      user: 'Monki Punk',
      core: '推广Web3边玩边赚游戏项目',
      trans: '嘿伙计，希望你过得愉快！我们团队正在构建一个全新的Web3边玩边赚项目——一个...'
    },
    {
      user: '@Ikoweb3',
      core: 'KOL和增长顾问，拥有6万+粉丝，管理500+加密影响者网络，提供营销服务',
      trans: '你好FinTax，我是Iko (@Ikoweb3)，KOL和增长顾问，拥有6万+粉丝，是@GemBooster的合作伙伴...'
    },
    {
      user: 'Molly Clarkk',
      core: '开玩笑询问是否参加了昨天的精子竞赛',
      trans: '嘿嘿，你昨天参加精子竞赛了吗？哈哈'
    },
    {
      user: 'Haileyyy',
      core: '询问能否问一个问题',
      trans: '我能问你一个问题吗？'
    }
  ],
  'x（CN） ': [
    {
      user: 'Lucyy',
      core: '猜测对方要么会连发消息要么会已读不回',
      trans: '不骗你，我觉得你要么会连发消息，要么会让人已读不回😭'
    },
    {
      user: 'Sunny in Silicon Valley',
      core: '赞赏FinTax专业度，提议分享AI增长技巧',
      trans: '你好FinTax，看了你的主页，你们在加密货币财税领域的专业度真的很让人印象深刻！特别是看到创始人@Calixbit的背景，感觉你们正在做一件很有价值的事情。最近我们也在研究如何帮助像你们这样的专业账号更高效地增长X平台影响力，发现了一些有趣的AI小技巧，或许能帮你们在保持专业调性的同时轻松获得更多关注。如果你感兴趣的话，我们可以交流下心得~'
    },
    {
      user: 'Emma',
      core: '打招呼',
      trans: '怎么样？'
    },
    {
      user: 'Lucyy',
      core: '询问能否告诉对方一些事情',
      trans: '我能告诉你一些事吗？'
    },
    {
      user: 'Remz/Assistant',
      core: '冒充Lark Davis的诈骗消息，邀请加入加密货币交易群，提供WhatsApp联系方式',
      trans: '你好，我是推特上的Lark Davis。很高兴你关注了我并成为我的粉丝。我经常在推特上分享加密货币趋势和市场动态，希望与大家分享更多知识。许多粉丝给我发消息说想跟我学习交易。由于我无法单独回复每个人，我创建了一个加密货币群组以便于交流、互动和学习。我会在工作日每天在群聊中分析加密货币合约交易计划，以及我对加密货币信号的早期见解。如果你感兴趣，可以添加我的WhatsApp：+44 7715 827723 加入学习之旅。'
    },
    {
      user: '��えん坊のわっくん',
      core: '询问朋友是否有空聊天',
      trans: '嘿朋友，你现在有空聊天吗？'
    },
    {
      user: 'Lucy',
      core: '开玩笑询问打开相机时手机是否在暗中评判你',
      trans: '嘿嘿，你也觉得打开相机时手机在暗中评判你吗，还是只有我这样？:))'
    },
    {
      user: 'Molly Clark',
      core: '询问对方是否擅长发短信还是只擅长刷推特',
      trans: '你真的擅长发短信还是只擅长刷推特'
    },
    {
      user: 'Iko | Web3',
      core: 'KOL和增长顾问，拥有6万+粉丝，管理500+加密影响者网络，提供营销和融资服务',
      trans: '你好FinTax中文，我是Iko (@Ikoweb3)���KOL和增长顾问，拥有6万+粉丝，是@GemBooster的合作伙伴。我和我的团队在Kollektiv Deals管理着一个由500多名加密影响者组成的私人网络。我们开展快速有效的营销活动，从推广和社区增长到融资和交易所上市。我们曾与币安、Bybit、Gate、OKX、Fetch.ai合作，并支持了100多个Web3、DePIN、AI和DeFi项目。你愿意快速聊聊我们如何提升你项目的曝光度和吸引力吗？此致，Iko'
    },
    {
      user: 'MC_ETH',
      core: '询问能否问几个问题',
      trans: '嘿伙计，介意我问你几个问题吗？'
    }
  ],
  '领英': [
    {
      user: 'Peter Saddington',
      core: '在Bitcoin Vegas见面后跟进，推广BitcoinRacing项目和Netflix纪录片',
      trans: '在Bitcoin Vegas见到你了！我们正在寻找希望接触无限学生群体、网络效应并在大型媒体上曝光的进步公司。查看www.BitcoinRacing.us了解更多信息，并在这里预览我们向Netflix推介的纪录片第1集：https://youtu.be/cFv__0EOrVw。这是一个先机优势。最好的，Peter Saddington'
    },
    {
      user: 'Sunny in Silicon Valley',
      core: 'MetaMerch加密商品公司寻求合作伙伴联系人',
      trans: '你好FinTax团队，我是MetaMerch的Aryan——领先的加密商品公司。我们设计和生产卓越的、可定制的加密商品，包括服装、配饰等，以赋能Web3领导者通过优质产品放大他们的营销策略和品牌影响力。你能否将我引荐给负责合作伙伴关系的人？'
    }
  ]
};

// 读取Excel文件
const workbook = XLSX.readFile('推特及领英25年10月至26年03月私信内容.xlsx');

console.log('开始处理Excel文件...\n');

// 处理每个工作表
Object.keys(translations).forEach(sheetName => {
  console.log(`处理工作表: ${sheetName}`);
  const worksheet = workbook.Sheets[sheetName];
  
  if (!worksheet) {
    console.log(`  工作表不存在，跳过`);
    return;
  }
  
  const data = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });
  const headers = data[0];
  
  // 找到列索引
  let userCol = headers.indexOf('用户名');
  const coreCol = headers.indexOf('核心信息');
  const transCol = headers.indexOf('中文翻译');
  
  // 特殊处理：x（CN）工作表的第一列不是"用户名"，需要修复表头
  if (sheetName === 'x（CN） ' && userCol === -1) {
    console.log(`  修复工作表表头...`);
    data[0][0] = '用户名';
    userCol = 0;
  }
  
  console.log(`  找到列 - 用户名:${userCol}, 核心信息:${coreCol}, 中文翻译:${transCol}`);
  
  // 处理每条翻译数据
  translations[sheetName].forEach(item => {
    // 查找对应的行
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      if (row[userCol] === item.user) {
        row[coreCol] = item.core;
        row[transCol] = item.trans;
        console.log(`  ✓ 已更新: ${item.user}`);
        break;
      }
    }
  });
  
  // 将数据写回工作表
  const newWorksheet = XLSX.utils.aoa_to_sheet(data);
  workbook.Sheets[sheetName] = newWorksheet;
});

// 保存修改后的文件
XLSX.writeFile(workbook, '推特及领英25年10月至26年03月私信内容.xlsx');
console.log('\n✅ 处理完成！文件已更新。');
