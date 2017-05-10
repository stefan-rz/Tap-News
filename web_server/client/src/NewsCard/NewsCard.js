import './NewsCard.css';
import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component{
  constructor(props) {
   super(props);
   this.state = {isToggleLikeOn: false, isToggleDisLikeOn: false};
 }

 handleLikeClick(e) {
     this.setState(prevState => ({
     isToggleLikeOn: !prevState.isToggleLikeOn
   }));
     console.log(this.state.isToggleLikeOn)
     this.sendClickLog()
      e.preventDefault(); // Now link won't go anywhere
 }

 handleDisLikeClick(e) {
     this.setState(prevState => ({
     isToggleDisLikeOn: !prevState.isToggleDisLikeOn
   }));
      this.sendClickLog()
     e.preventDefault(); // Now link won't go anywhere

}

  redirectToUrl(e, url) {
    this.sendClickLog();
    window.open(url, '_blank');
    e.preventDefault(); // Now link won't go anywhere
  }

  sendClickLog() {
    let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
              + '/newsId/' + this.props.news.digest + '/isLikeOn/' + this.state.isToggleLikeOn
    + '/isDislikeOn/' + this.state.isToggleDisLikeOn;

    let request = new Request(encodeURI(url), {
      method: 'POST',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      },
      cache: false});

    fetch(request);
  }

  render() {
    return(
      <div className="news-container">
        <div className='row'>
          <div className='col s4 fill hover-col'>
            <img src={this.props.news.urlToImage} alt='news'/>
            <div className='outer'>
                <div className='inside'>
                    <a className="list-group-item" href='#' onClick={(e) => this.handleLikeClick(e)}>
                        <i className='fa fa-heart fa-1x' aria-hidden='true'>{this.state.isToggleLikeOn ? 'Remove Like' : 'Like'}</i>
                    </a>
                    <a className="list-group-item" href="#" onClick={(e) => this.handleDisLikeClick(e)}>
                        <i className='fa fa-ban fa-1x' aria-hidden='true'>{this.state.isToggleDisLikeOn ? 'Remove DisLike' : 'DisLike'}</i>
                    </a>
                </div>
            </div>
          </div>
          <div className="col s8" onClick={(e) => this.redirectToUrl(e, this.props.news.url)}>
            <div className="news-intro-col">
              <div className="news-intro-panel">
                <h4>{this.props.news.title}</h4>
                <div className="news-description">
                  <p>{this.props.news.description}</p>
                  <div>
                    {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                    {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                    {this.props.news.time != null && <div className='chip amber news-chip'>{this.props.news.time}</div>}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default NewsCard;
