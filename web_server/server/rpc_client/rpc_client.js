var jayson = require('jayson');
var load_config = require('../config/config')
var cf = load_config.load_config().web_server.server.rpc_client
var client = jayson.client.http({
    port: cf.port,
    hostname: cf.hostname
});

// Test RPC method
function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Log a news click event for a user
function logNewsClickForUser(user_id, news_id, isLikeOn, isDisLikeOn) {
    client.request('logNewsClickForUser', [user_id, news_id, isLikeOn, isDisLikeOn], function(err, error, response) {
        if (err) throw err;
        console.log(response);
    });
}

module.exports = {
    add : add,
    getNewsSummariesForUser : getNewsSummariesForUser,
    logNewsClickForUser : logNewsClickForUser
}
