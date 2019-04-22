import React, {Component} from 'react';
import {connect} from 'react-redux';
import {updatePage} from '../actions';
import {Pagination} from 'react-bootstrap';


class PageWindow extends Component {

    highlight = () => {
        // Данный метод подсвечивает все вхождения выбранного символа на странице.
        // Он реализован, наивно полагая, что у нас не будет пересекающихся вхождений.
        // Разумеется, они будут, и нужно подумать как именно их отображать.

        let { text_chunk, existences, symbol, start_position } = this.props;
        let exs_to_highlight = existences && symbol && existences[symbol.value];
        let new_chunk = '';

        if (exs_to_highlight) {
            console.log(exs_to_highlight)
            console.log(start_position)

            let sort_existences = exs_to_highlight.map((exs) => {
                let start = (exs[0] + exs[1]) - start_position;
                let end = (start + exs[2]);
                return [start, end];
            }).sort((a,b) => a[0] > b[0]);

            let prev = 0
            for (let i = 0; i < sort_existences.length; i++) {
                new_chunk += text_chunk.slice(prev, sort_existences[i][0]);
                let text_symbol = text_chunk.slice(sort_existences[i][0], sort_existences[i][1]);
                new_chunk += `<span style="color:red; background-color: RGB(249, 201, 16);">${text_symbol}</span>`;
                prev = sort_existences[i][1];
            }
            new_chunk += text_chunk.slice(prev, text_chunk.length);
            return new_chunk;

        } else {
            return text_chunk;
        }
    }

    render() {
        const {number_pages, page, updatePage} = this.props;
        const text_chunk = this.highlight();

        return(
            <div>
                <div id='page-window' dangerouslySetInnerHTML={{__html: text_chunk}} />
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
