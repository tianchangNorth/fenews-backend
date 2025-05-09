import axios from 'axios';
// import dotenv from 'dotenv';
// import { fileURLToPath } from 'url';
// import { dirname, resolve } from 'path';

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = dirname(__filename);
// dotenv.config({ path: resolve(__dirname, '../.env') });
// dotenv.config();
export async function chatWithAI(prompt) {
  console.log(`\n\n🤖 AI 请求: ${prompt}`);

  try {
    const res = await axios.post(
      'https://api.deepseek.com/chat/completions',
      {
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: '请你作为技术编辑，为下面的文章从 0 到 10 打一个分，保留一位小数。评分越高代表内容越有深度、技术含量越高、有价值。只返回一个数字，不要解释' },
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
