import React, {Component} from 'react';
import {connect} from 'react-redux';
import {updatePage} from '../actions';
import {Pagination} from 'react-bootstrap';
import {BLACK, WHITE, SQUARE_BRACKET, COLOR_SCHEME} from '../utils';


class PageWindow extends Component {

    get_span = (text, exs_id, add_class='') => {
        let color = COLOR_SCHEME[exs_id % 7] || BLACK;
        let styles = `color:${color};`;
        if (color != BLACK) {
            text = `${text}`;
            styles += 'cursor:pointer;text-decoration:underline;';
        }
        let classes = `exs exs-${exs_id}`;
        if (add_class) {
            classes += ` ${add_class}`;
        }
    
        return `<span style="${styles}" data-color="${color}" class="${classes}">${text}</span>`;
    }

    highlight = () => {
        let { text_chunk, existences, symbol, start_position, selected_text_coordinates } = this.props;
        let exs_to_highlight = existences && symbol && existences[symbol.value];
        let new_chunk = '';
        let has_coordinates = Object.keys(selected_text_coordinates).length > 0;

        if (has_coordinates) {
            let start_context = selected_text_coordinates.start;
            let start_selected_text = selected_text_coordinates.word_shift;
            let end_selected_text = start_selected_text + selected_text_coordinates.word_len;
            let end_context = selected_text_coordinates.end;

            let first_part = text_chunk.slice(start_context, start_selected_text);
            let selected_text = text_chunk.slice(start_selected_text, end_selected_text);
            let second_part = text_chunk.slice(end_selected_text, end_context);

            new_chunk += `<span>${text_chunk.slice(0, start_context)}</span>`;
            new_chunk += `<span style="background-color: #ddd">${first_part}`;
            new_chunk += `<span style="color:#000; background-color: #FF0000;">${selected_text}</span>`;
            new_chunk += `${second_part}</span>`;
            new_chunk += `<span>${text_chunk.slice(end_context, text_chunk.length - 1)}</span>`;
            return new_chunk;
        }
                
        if (exs_to_highlight) {
            let positions = {};
            exs_to_highlight.map((exs, i) => {
                let start = (exs[0] + exs[1]) - start_position;
                let end = (start + exs[2]);
                positions[start] = ['[', i];
                positions[end] = [']', i];
            })

            let my_color_stack = [];
            let tmp_chunk = '';
            let current_exs_text = '';

            for (let i = 0; i < text_chunk.length; i++) {
                if (i in positions) {
                    let symbol = positions[i][0];
                    let exs_id = my_color_stack[my_color_stack.length - 1];
                    new_chunk += this.get_span(tmp_chunk, exs_id)

                    if (symbol == '[') {
                        new_chunk += this.get_span(symbol, positions[i][1], SQUARE_BRACKET);
                        tmp_chunk = text_chunk[i];
                        my_color_stack.push(positions[i][1]);
                    } else {
                        new_chunk += this.get_span(symbol, positions[i][1], SQUARE_BRACKET);

                        let ind = my_color_stack.indexOf(positions[i][1]);
                        if (ind != -1) {
                            my_color_stack.splice(ind, 1);
                        }
                        tmp_chunk = text_chunk[i];
                    }
                } else {
                    tmp_chunk += text_chunk[i];
                }
            }
            let exs_id = my_color_stack[my_color_stack.length - 1];
            new_chunk += this.get_span(tmp_chunk, exs_id);
            
            return new_chunk;
        } else {
            return text_chunk;
        }
    }

    get_target_class_name = (e) => {
        let target = e.relatedTarget;
        if (target) {
            if (target.tagName == 'U') {
                target = target.parentElement;
            }
            
            if (target.tagName == 'SPAN' && !target.classList.contains('exs-undefined') && !target.classList.contains(SQUARE_BRACKET)) {
                return target.classList[1];
            }
        }
    }

    mouseHandler = (e, is_out) => {
        // Подумать над тем, чтобы всё же реагировать на клик, а не наведение.
        // События наведения иногда "проскакивают"

        let className = this.get_target_class_name(e);
        if (className) {
            let exs_spans = document.getElementsByClassName('exs');
            for (let exs_span of exs_spans) {
                exs_span.style.color = is_out ? BLACK : exs_span.dataset.color;
                if (!exs_span.classList.contains('exs-undefined')) {
                    exs_span.style.textDecoration = is_out ? '' : 'underline';
                }
            }

            let elems = document.getElementsByClassName(className);
            let currEl = elems[0];
            let lastEl = elems[elems.length - 1];
            while (true) {
                if (!currEl.classList.contains(SQUARE_BRACKET)) {
                    currEl.style.color = is_out ? BLACK : currEl.dataset.color;
                    currEl.style.backgroundColor = is_out ? 'orange' : '';
                    currEl.style.textDecoration = is_out ? '' : 'underline';
                }
                if (currEl == lastEl) {
                    break;
                }
                currEl = currEl.nextElementSibling;
            }

            let brackets = document.getElementsByClassName(SQUARE_BRACKET);
            for (let b of brackets) {
                b.style.display = is_out ? 'none' : '';
            }
        }
    }

    onMouseOver = (e) => {
        this.mouseHandler(e, false);
    }

    onMouseOut = (e) => {
        this.mouseHandler(e, true);
    }

    render() {
        const {number_pages, page, updatePage} = this.props;
        const text_chunk = this.highlight();

        return(
            <div>
                <div 
                    id='page-window' 
                    dangerouslySetInnerHTML={{__html: text_chunk}} 
                    onMouseOut={this.onMouseOut} 
                    onMouseOver={this.onMouseOver}
                />
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
