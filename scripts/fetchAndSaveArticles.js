import { execFile } from 'child_process'
import mongoose from 'mongoose'
import Article from '../models/article.js'
import '../utils/loadEnv.js'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'
import { promisify } from 'util'

const execFileAsync = promisify(execFile)

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const pythonScriptPath1 = resolve(__dirname, '../crawlers/juejin.py')
const pythonScriptPath2 = resolve(__dirname, '../crawlers/medium.py')

async function runScript(scriptPath) {
  try {
    const { stdout } = await execFileAsync('python', [scriptPath])
    return JSON.parse(stdout)
  } catch (err) {
    console.error(`❌ 执行 ${scriptPath} 出错：`, err.message)
    return []
  }
}

async function main() {
  await mongoose.connect(process.env.MONGO_URI)
  await Article.deleteMany({})
  console.log('🚀 MongoDB 已连接，开始调用爬虫脚本...')

  const results1 = await runScript(pythonScriptPath1)
  const results2 = await runScript(pythonScriptPath2)

  const allArticles = [...results1, ...results2]

  for (const item of allArticles) {
    const exists = await Article.findOne({ url: item.url })
    if (!exists) {
      const source = item.url.includes('juejin.cn') ? 'juejin' : 'medium'
      await Article.create({ ...item, source })
      console.log('✅ 插入成功:', item.title)
    } else {
      console.log('⏭ 已存在:', item.title)
    }
  }

  console.log('🏁 资讯入库完成')
  mongoose.disconnect()
}

main()
