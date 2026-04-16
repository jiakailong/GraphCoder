const mysql = require('mysql2');
const dbConfig = require('./src/config/database');

// 创建连接池
const pool = mysql.createPool({
  host: dbConfig.host,
  port: dbConfig.port,
  user: dbConfig.user,
  password: dbConfig.password,
  charset: dbConfig.charset,
  connectionLimit: 10 // 连接池大小
});

// 获取数据库连接
const getConnection = () => {
  return new Promise((resolve, reject) => {
    pool.getConnection((err, connection) => {
      if (err) {
        reject(err);
      } else {
        resolve(connection);
      }
    });
  });
};

// 执行查询
const executeQuery = (sql, params = []) => {
  return new Promise(async (resolve, reject) => {
    try {
      const connection = await getConnection();
      connection.execute(sql, params, (err, results) => {
        connection.release(); // 释放连接回池
        if (err) {
          reject(err);
        } else {
          resolve(results);
        }
      });
    } catch (error) {
      reject(error);
    }
  });
};

module.exports = {
  executeQuery
};
