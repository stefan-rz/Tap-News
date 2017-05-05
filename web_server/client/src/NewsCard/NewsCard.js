import './NewsCard.css';
import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component{
  constructor(props) {
   super(props);
   this.state = {isToggleOn: true};

   // This binding is necessary to make `this` work in the callback
   this.handleClick = this.handleClick.bind(this);
 }

 handleClick() {
   this.setState(prevState => ({
     isToggleOn: !prevState.isToggleOn
   }));
 }


  redirectToUrl(url) {
    this.sendClickLog();
    window.open(url, '_blank');
  }

  sendClickLog() {
    let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
              + '/newsId/' + this.props.news.digest;

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
          <div className='col s4 fill hover-container'>
            <img src={this.props.news.urlToImage} alt='news'/>
            <i onClick={this.handleClick} className={this.state.isToggleOn ? 'fa fa-thumbs-up' : 'fa fa-thumbs-down'}></i>
          </div>
          <div className="col s8" onClick={() => this.redirectToUrl(this.props.news.url)}>
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
