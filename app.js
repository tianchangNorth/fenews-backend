import express from 'express'
import mongoose from 'mongoose'
import dotenv from 'dotenv'
import articleRoutes from './routes/articles.js'; // 引入刚才创建的路由

dotenv.config()

const app = express()
app.use(express.json())

// 连接 MongoDB
mongoose.connect(process.env.MONGO_URI).then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.error('❌ MongoDB connection error:', err))

app.use((req, res, next) => {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    next();
});

// 示例路由
app.use('/api', articleRoutes);

app.listen(3000, () => {
  console.log('🚀 Server running at http://localhost:3000')
})
