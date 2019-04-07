import React, {Component} from 'react';
import {connect} from 'react-redux';
import {updatePage} from '../actions';
import {Pagination} from 'react-bootstrap';


class PageWindow extends Component {

    updatePage = (page) => {
        this.props.updatePage(page);
    }

    render() {
        const {text_chunk, number_pages, page} = this.props;

        return(
            <div>
                <div id='page-window'>
                    {text_chunk}
                </div>
                <Pagination 
                    prev
                    next
                    ellipsis
                    boundaryLinks
                    bsSize='small'
                    items={number_pages}
                    maxButtons={6}
                    activePage={page}
                    onSelect={this.updatePage}
                />
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        book_id: state.editor.book_id,
        page: state.editor.page,
        number_pages: state.editor.number_pages,
        text_chunk: state.editor.text_chunk,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updatePage: (page) => dispatch(updatePage(page)),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(PageWindow);
