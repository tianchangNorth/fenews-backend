import mongoose from 'mongoose'

const ArticleSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
  },
  url: {
    type: String,
    required: true,
    unique: true, // 防止重复抓取同一篇
  },
  img: String,        // 图片（如果能爬）
  brief: String,      // 简要内容
  // content: String,    // 正文（如果能爬）
  tags: [String],     // AI 生成的标签
  summary: String,    // AI 生成的摘要
  score: {
    type: Number,
    default: 0,
  },      // AI 给出的价值评分（例如 1-10）
  createdAt: {
    type: Date,
    default: Date.now,
  },
  source: {
    type: String,
    default: 'juejin',
  }
})

export default mongoose.model('Article', ArticleSchema)
