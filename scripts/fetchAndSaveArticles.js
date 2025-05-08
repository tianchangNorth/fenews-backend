import { execFile } from 'child_process'
import mongoose from 'mongoose'
import dotenv from 'dotenv'
import Article from '../models/article.js'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

// 获取当前文件目录
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const pythonScriptPath = resolve(__dirname, '../crawlers/juejin.py')
// 显式指定 .env 路径
dotenv.config({ path: resolve(__dirname, '../.env') })

async function main() {
  await mongoose.connect(process.env.MONGO_URI)
  await Article.deleteMany({}); // 清空数据库中的数据
  console.log('🚀 MongoDB 已连接，开始调用爬虫脚本...')

  execFile('python', [pythonScriptPath], async (err, stdout) => {
    if (err) {
      console.error('❌ 爬虫执行失败：', err)
      process.exit(1)
    }

    try {
      const articles = JSON.parse(stdout)

      for (const item of articles) {
        const exists = await Article.findOne({ url: item.url })
        if (!exists) {
          await Article.create({ ...item, source: 'juejin' })
          console.log('✅ 插入成功:', item.title)
        } else {
          console.log('⏭ 已存在:', item.title)
        }
      }

      console.log('🏁 资讯入库完成')
      mongoose.disconnect()
    } catch (e) {
      console.error('❌ JSON 解析失败：', e.message)
    }
  })
}

main()
