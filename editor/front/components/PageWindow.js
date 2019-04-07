import React, {Component} from 'react';
import {connect} from 'react-redux';
import * as actions from '../actions'


class PageWindow extends Component {
    render() {
        return(
            <div>
                {this.props.text_chunk}
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        book_id: state.editor.book_id,
        page: state.editor.page,
        text_chunk: state.editor.text_chunk,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        get_contexts: () => dispatch(get_contexts()),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(PageWindow);
