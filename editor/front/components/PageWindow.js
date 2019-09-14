import React, {Component} from 'react';
import {connect} from 'react-redux';
import {updatePage} from '../actions';
import {Pagination} from 'react-bootstrap';
import {BLACK, WHITE, SQUARE_BRACKET, COLOR_SCHEME, ALL_SYMBOLS} from '../utils';


class PageWindow extends Component {

    get_span = (text, exs_id, symbol_id, add_class='') => {
        let color = COLOR_SCHEME[symbol_id % 35] || BLACK;
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

        let exs_to_highlight = []
        // Если выбран вариант "Все символы", то подсвечиваем всё
        if (!symbol || symbol.value == ALL_SYMBOLS.value) {
            for (let key in existences) {
                for (let ex of existences[key]) {
                    exs_to_highlight.push(ex.concat([Number(key)]));
                }
            }
        } else if (existences && symbol && existences[symbol.value]) {
            for (let ex of existences[symbol.value]) {
                exs_to_highlight.push(ex.concat([Number(symbol.value)]));
            }
        }   

        let new_chunk = '';
        let has_coordinates = Object.keys(selected_text_coordinates).length > 0;

        if (has_coordinates) {
            // Подсветка "пользовательского" выделения
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
                
        if (exs_to_highlight && exs_to_highlight.length) {
            let positions = {};
            exs_to_highlight.map((exs, i) => {
                let start = (exs[0] + exs[1]) - start_position;
                let end = (start + exs[2]);
                positions[start] = {'character': '[', 'exs_number': i, 'symbol_id': exs[4]};
                positions[end] = {'character': ']', 'exs_number': i, 'symbol_id': exs[4]};
            })

            let my_color_stack = [];
            let tmp_chunk = '';
            let current_exs_text = '';

            for (let i = 0; i < text_chunk.length; i++) {
                if (i in positions) {
                    let {character, exs_number, symbol_id} = positions[i];
                    let data = my_color_stack[my_color_stack.length - 1];

                    new_chunk += this.get_span(tmp_chunk, data && data[0], data && data[1])
                    new_chunk += this.get_span(character, exs_number, symbol_id, SQUARE_BRACKET);
                    tmp_chunk = text_chunk[i];

                    if (character == '[') {
                        my_color_stack.push([exs_number, symbol_id]);
                    } else {
                        let ind = -1;
                        for (let el in my_color_stack) {
                            if (my_color_stack[el][1] == symbol_id) {
                                ind = el;
                                break
                            }
                        }
                        if (ind != -1) {
                            my_color_stack.splice(ind, 1);
                        }
                    }
                } else {
                    tmp_chunk += text_chunk[i];
                }
            }
            let data = my_color_stack[my_color_stack.length - 1];
            new_chunk += this.get_span(tmp_chunk, data && data[0], data && data[1]);
            
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

const mapStateToProps = state => {
    const editor = state.editor;

    return {
        page: editor.page,
        number_pages: editor.number_pages,
        text_chunk: editor.text_chunk,
        symbol: editor.symbol,
        existences: editor.existences,
        start_position: editor.start_position,
        selected_text_coordinates: editor.selected_text_coordinates,
    }
}

const mapDispatchToProps = dispatch => {
    return { 
        updatePage: (page) => dispatch(updatePage(page)) 
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(PageWindow);
