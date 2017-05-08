var client = require('./rpc_client');

//Start Redis, MongoDB and recommandation_service, rpc service, news_topic_modeling service in backend before running following tests
// invoke 'add'
client.add(1, 2, function(response) {
    console.assert(response == 3);
});

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('test_user', 1, function(response) {
  console.assert(response != null);
});

// invoke "logNewsClickForUser"
client.logNewsClickForUser('test_user', 'test_news');
