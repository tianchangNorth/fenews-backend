import mongoose from 'mongoose';

const processedArticleSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    url: { type: String, required: true, unique: true },
    content: { type: String }, // 原文内容（可选）
    summary: { type: String }, // AI 生成的摘要
    tags: [String],            // AI 提取的标签/关键词
    categories: [String],      // 分类标签（如：前端、Node.js 等）
    source: { type: String },  // 原始来源（如：掘金）
    createdAt: { type: Date, default: Date.now },
    processedAt: { type: Date, default: Date.now },
  },
  {
    collection: 'processed_articles',
  }
);

export default mongoose.model('ProcessedArticle', processedArticleSchema);
