import './NewsCard.css';
import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isToggleLikeOn: this.props.news.isLikeToggleOn, isToggleDislikeOn: this.props.news.isDislikeToggleOn};
    }

    handleLikeClick(e) {
        this.setState(prevState => ({
            isToggleLikeOn: !prevState.isToggleLikeOn
        }));
        e.preventDefault(); // Now link won't go anywhere
    }

    handleDisLikeClick(e) {
        this.setState(prevState => ({
            isToggleDislikeOn: !prevState.isToggleDislikeOn
        }));
        e.preventDefault(); // Now link won't go anywhere

    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.isToggleLikeOn === true && this.state.isToggleLikeOn !== prevState.isToggleLikeOn
            && this.state.isToggleDislikeOn === true) {
            this.setState({isToggleDislikeOn: false});
        } else if (this.state.isToggleDislikeOn === true && this.state.isToggleDislikeOn
            !== prevState.isToggleDislikeOn && this.state.isToggleLikeOn === true) {
            this.setState({isToggleLikeOn: false});
        }

        if (this.state.isToggleLikeOn !== prevState.isToggleLikeOn ||
            this.state.isToggleDislikeOn !== prevState.isToggleDislikeOn) {
            this.sendClickLog();
            console.log("isToggleLikeOn: " + this.state.isToggleLikeOn);
            console.log("isToggleDislikeOn: " + this.state.isToggleDislikeOn);
        }


    }

    redirectToUrl(e, url) {
        this.sendClickLog();
        window.open(url, '_blank');
        e.preventDefault(); // Now link won't go anywhere
    }

    sendClickLog() {
        let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
            + '/newsId/' + this.props.news.digest + '/isLikeToggleOn/' + this.state.isToggleLikeOn
            + '/isDislikeToggleOn/' + this.state.isToggleDislikeOn

        let request = new Request(encodeURI(url), {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request);
    }

    render() {
        return (
            <div className="news-container">
                <div className='row'>
                    <div className='col s4 fill hover-col'>
                        <img src={this.props.news.urlToImage} alt='news'/>
                        <div className='outer'>
                            <div className='inside'>
                               <a onClick={(e) => this.handleLikeClick(e)}><i className='fa fa-heart fa-2x fa-fw'
                                       aria-hidden='true'></i>&nbsp; {this.state.isToggleLikeOn ? 'Remove Like' : 'Like'}
                               </a>
                               <a onClick={(e) => this.handleDisLikeClick(e)}><i className='fa fa-ban fa-2x fa-fw'
                                                                                 aria-hidden='true'></i>
                                   &nbsp; {this.state.isToggleDislikeOn ? 'Remove DisLike' : 'DisLike'}
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
                                        {this.props.news.source != null &&
                                        <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                                        {this.props.news.reason != null &&
                                        <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                                        {this.props.news.time != null &&
                                        <div className='chip amber news-chip'>{this.props.news.time}</div>}
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
