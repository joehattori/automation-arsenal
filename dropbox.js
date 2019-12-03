const dropboxPath = process.argv[process.argv.length - 1];
const paths = dropboxPath.split("/");
const saveFileName = paths[paths.length - 1];
const dotenv = require("dotenv");
dotenv.config();
const token = process.env.DROPBOX_ACCESS_TOKEN;
if (!token) {
    console.error("Please set token.");
    return;
}
const fs = require("fs");
const Dropbox = require("dropbox").Dropbox;

const fetch = require("isomorphic-fetch");
const dbx = new Dropbox({
    fetch: fetch,
    accessToken: token,
});

const files = dbx.filesDownload({
    path: dropboxPath,
}).then(function(result){
    fs.writeFile(saveFileName, result.fileBinary, "binary", function(error) {
        if (error) {
            console.error("Error occurred: ", error);
        } else {
            console.log(`Successfully downloaded to ${saveFileName}`);
        }
    });
}, console.error);
