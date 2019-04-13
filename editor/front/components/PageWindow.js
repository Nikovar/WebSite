import React, {Component} from 'react';
import {connect} from 'react-redux';
import {updatePage} from '../actions';
import {Pagination} from 'react-bootstrap';


class PageWindow extends Component {

    render() {
        const {text_chunk, number_pages, page, updatePage} = this.props;

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
                    onSelect={updatePage}
                />
            </div>
        )
    }
}

export default PageWindow;
