import express from 'express';
import Article from '../models/article.js'; // 引入 Article 模型

const router = express.Router();

// 获取文章列表接口
router.get('/articles', async (req, res) => {
  try {
    // 你可以根据需求调整查询条件
    const articles = await Article.find({}).limit(20).sort({ createdAt: -1 });
    res.json(articles); // 返回文章列表
  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ error: 'Failed to fetch articles' });
  }
});

export default router;
