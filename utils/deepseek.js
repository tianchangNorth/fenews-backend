import axios from 'axios';
// import dotenv from 'dotenv';
// import { fileURLToPath } from 'url';
// import { dirname, resolve } from 'path';

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = dirname(__filename);
// dotenv.config({ path: resolve(__dirname, '../.env') });
// dotenv.config();
export async function chatWithAI(prompt) {
  console.log(`🤖 AI 请求: ${prompt}`);

  try {
    const res = await axios.post(
      'https://api.deepseek.com/chat/completions',
      {
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: '你是一个技术资讯助手，只返回一个 JSON 数组，格式如下：["关键词1", "关键词2", "关键词3"]。不要包含其它内容。' },
          { role: 'user', content: prompt },
        ],
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return res.data.choices?.[0]?.message?.content?.trim();

  } catch (err) {
    console.error('❌ 调用 DeepSeek 出错：', err?.response?.data || err.message);
    return [];
  }
}
