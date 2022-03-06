const AWS = require('aws-sdk')
const sm = new AWS.SecretsManager({region:'us-east-1'})  // 建立sm ，用AWS 呼叫物件 SecretsManager

const getSecrets= async(SecretId)=>{                         // 建立非同步連線子程式
    return await new Promise((resolve, reject) =>{           // Promise回傳參數，成功res，失敗rej
        sm.getSecretValue({ SecretId },(err,result) => {    //  sm 呼叫物件getSecretValue，成功會得到{SecretId}
            if (err) reject(err)
            else resolve(JSON.parse(result.SecretString))
        })
    })
}

const main =async(event) =>{
    console.log('Event:',event);
    const { apikey } = await getSecrets(                      // 若成功，子程式傳回 {SecretId}(json格式)
        process.env.prod ? 'test_prod_secrets' : 'test_dev_secrets'  // 待確認: 如果環境變數使用中，回傳test_p內的apikey的值，沒有的話傳test_d
    )
    return apikey
}

exports.handler = main