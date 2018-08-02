var fs = require('fs');
console.log(process.argv[2]);

fs.readFile(process.argv[2], (err, data) => {
  if (err) console.log('err');
  else {
    data.toString().split('\n').map((e, i) => {
      // console.log(i);
      console.log(e);
      let readfilename = "kettle_config/" + e + "/" + e + "处理数据文件.ktr";
      console.log(readfilename);
      let writefilename = "kettle_config/" + e + "/_" + e + "处理数据文件.ktr";
      fs.readFile(readfilename, function(err, data) {
        if(err) console.log('文件读取发生错误');
        else {
            let s = data.toString();
            let encodedStr = s.replace(/[\u00A0-\u9999<>\&]/gim, function(i) {
              // console.log(i)
              switch (i) {
                case '<': case '>':
                  return i;
                default:
                  return '&#x'+i.charCodeAt(0).toString(16)+';';
              }  
            });
            fs.writeFile(writefilename, encodedStr);
        }
      });
    });
  }
});