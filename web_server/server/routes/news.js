var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

 /* GET news list. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  console.log('Fetching news...');
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];
  rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
    res.json(response);
  });
});

/* POST news click event. */
router.post('/userId/:userId/newsId/:newsId/isLikeToggleOn/:isToggleLikeOn/isDislikeToggleOn/:isToggleDislikeOn', function(req,res, next) {
  console.log('Logging news click...');
  user_id = req.params['userId'];
  news_id = req.params['newsId'];
  isLikeToggleOn = req.params['isToggleLikeOn'];
  isDislikeToggleOn = req.params['isToggleDislikeOn'];

  rpc_client.logNewsClickForUser(user_id, news_id, isLikeToggleOn, isDislikeToggleOn);
  res.status(200).end();
});

module.exports = router;
