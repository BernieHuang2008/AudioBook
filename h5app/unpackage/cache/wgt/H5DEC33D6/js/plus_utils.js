function plus_io_dir(path, callback) {
    if (typeof plus === "undefined" || !plus.io) {
        console.error("plus.io is not available.");
        return;
    }

    plus.io.resolveLocalFileSystemURL(plus.io.convertLocalFileSystemURL(path), function(dirEntry) {
        var directoryReader = dirEntry.createReader();
        directoryReader.readEntries(function(entries) {
            var files = [];
            for (var i = 0; i < entries.length; i++) {
                if (entries[i].isDirectory) {
                    files.push(entries[i].name);
                }
            }
            callback(files);
        }, function(error) {
            console.error("Error reading directory entries:", error);
        });
    });
}

function plus_io_writeFile(path, data) {
	return new Promise(resolve => { //这里封装了个是一个promise异步请求
		// plus.io.requestFileSystem是请求本地文件系统对象
		plus.io.requestFileSystem(
			plus.io.PRIVATE_DOC, // 文件系统中的根目录下的DOCUMENTS目录
			fs => {
				// 创建或打开文件, fs.root是根目录操作对象,直接fs表示当前操作对象
				fs.root.getFile(path, {
					create: true // 文件不存在则创建
				}, fileEntry => {
					// 文件在手机中的路径
					// console.log(fileEntry.fullPath)
					fileEntry.createWriter(writer => {
						// 写入文件成功完成的回调函数
						writer.onwrite = e => {
							console.log("写入本地文件成功");
							resolve("写入本地文件")
						};
						// 写入数据
						writer.write(data);
					})
				}, e => {
					console.log("getFile failed: " + e.message);
				});
			},
			e => {
				console.log(e.message);
			}
		);
	})
}

function plus_io_readFile(path) {
	return new Promise(resolve => { //文件读写是一个异步请求 用promise包起来方便使用时的async+await
		plus.io.requestFileSystem(
			plus.io.PRIVATE_DOC,
			fs => {
				fs.root.getFile(path, {
					create: false
				}, fileEntry => {
					fileEntry.file((file) => {
						console.log("文件大小:" + file.size + '-- 文件名:' + file.name);
						//创建读取文件对象
						let fileReader = new plus.io.FileReader();
						//以文本格式读取文件数据内容
						fileReader.readAsText(file, 'utf-8');
						//文件读取操作完成时的回调函数
						fileReader.onloadend = (evt) => {
							resolve(evt.target.result)
						}
					});
				}, e => {
					console.log("getFile failed: " + e.message);
				});
			},
			e => {
				console.log(e.message);
			}
		);
	})
}