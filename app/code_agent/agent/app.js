const { executeQuery } = require('./db');

// 测试数据库连接
async function testConnection() {
  try {
    const result = await executeQuery('SELECT 1 + 1 AS solution');
    console.log('Database connection successful!');
    console.log('Result:', result[0].solution);
  } catch (error) {
    console.error('Database connection failed:', error);
  }
}

testConnection();
