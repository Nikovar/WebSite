import React, {Component} from 'react';
import Select from 'react-select';
import Creatable from 'react-select/lib/Creatable';
import AsyncSelect from 'react-select/lib/Async';
import {SQUARE_BRACKET, getContexts, getContextTypes} from '../utils';


export default class AddSymbolForm extends Component  {

    constructor(props) {
        super(props);
        this.state = this.getInitialState();
    }

    getInitialState = () => {
        return {
            symbol: {},
            contexts: [],
            start: 0,
            word_shift: 0,
            word_len: 0,
            end: 0,
            text: '',
            context_type: {},
            context_description: '',
            showForm: false
        }
    }

    onChangeSymbol = (e) => {
        let new_symbol = {
            value: e.__isNew__ ? 'new' : e.value, 
            label: e.label, 
        }

        this.setState({symbol: new_symbol});
    }

    getLocation = (text_nodes, anchorNode, anchorOffset, focusNode, focusOffset) => {
        const { text_chunk } = this.props;
        let start_selection = 0;
        let end_selection = 0;

        for (let node of text_nodes) {
            if (node == anchorNode) {
                start_selection += anchorOffset;
                break;
            } else {
                start_selection += node.data.toString().length;
            }
        }
        for (let node of text_nodes) {
            if (node == focusNode) {
                end_selection += focusOffset;
                break;
            } else {
                end_selection += node.data.toString().length;
            }
        }

        let word_shift = start_selection;

        let start = 0;
        let end = text_chunk.length;
        let end_characters = ['.', '?', '!'];

        for (let i = word_shift; i > 0; i--) {
            if (end_characters.includes(text_chunk[i])) {
                start = i + 1;
                break;
            }
        }

        // мы должны "захватывать" символ окончания предложения.
        // ниже мы обрабатываем ситуацию, когда предложение оканчивается, например, на ???
        let prev_symbol = '';
        for (let i = end_selection; i < text_chunk.length; i++) {
            if (end_characters.includes(text_chunk[i])) {
                prev_symbol = text_chunk[i];
            } else if (prev_symbol) {
                end = i;
                break;
            }
        }

        let word_len = end_selection - start_selection;
        return {start, word_shift, word_len, end}
    }
    
    onToggle = () => {
        const { symbolAddition, toggleSymbolAddition } = this.props;

        if (!symbolAddition) {
            let selection = window.getSelection();
            let page_window = document.getElementById('page-window');
            let text_nodes = [];
            for (let node of page_window.childNodes) {
                if (node.classList && node.classList.contains(SQUARE_BRACKET)) {
                    continue
                }
                
                if (node.childNodes.length > 0) {
                    text_nodes.push(node.childNodes[0]);
                } else {
                    text_nodes.push(node);
                }
            }

            const {anchorNode, anchorOffset, focusNode, focusOffset} = selection;
            let selected_text = selection.toString()
            
            if (selected_text && text_nodes.includes(anchorNode) && text_nodes.includes(focusNode)){
                let { start, word_shift, word_len, end } = this.getLocation(
                    text_nodes, 
                    anchorNode, 
                    anchorOffset, 
                    focusNode, 
                    focusOffset
                );
                this.props.selectTextCoordinates({ start, word_shift, word_len, end });

                this.setState({                    
                    text: selected_text,
                    start: start,
                    word_shift: word_shift,
                    word_len: word_len,
                    end: end
                });


            } else {
                alert('Прежде, чем добавить новый символ,\n' + 
                      'вы должны выделить текст на странице\n' +
                      'для определения контекста этого символа!');
                return
            }
        } else {
            this.setState(this.getInitialState());
            this.props.selectTextCoordinates({});
        }
        toggleSymbolAddition();
    }

    onSubmit = (e) => {
        e.preventDefault();
        if (!this.state.symbol.value) {
            alert('Выберите или добавьте новый символ!');
        } else {
            const {start_position} = this.props;
            const {
                symbol, start, word_shift, word_len, end, contexts, context_type, context_description
            } = this.state;

            let data = {
                symbol_id: symbol.value,
                symbol_title: symbol.label,
                start: start + start_position,
                word_shift: word_shift,
                word_len: word_len,
                end: end,
                context_ids: contexts.map(el => el.value),
                context_type: context_type && context_type.value,
                context_description: context_description,
            }
            this.props.tmpSaveSymbol(data);
            this.setState(this.getInitialState());
        }
    }

    render() {
        const {symbolAddition, symbols} = this.props;
        const {symbol, contexts, context_type, context_description} = this.state;

        if (!symbolAddition) {
            return <button onClick={this.onToggle}>Добавить символ</button>
        }

        return(
            <div id='add-information-form'>
                <div>
                    <div className="form-group">
                        <label htmlFor="symbol">Символ</label>
                        <Creatable
                            id='symbol'
                            value={symbol}
                            options={symbols}
                            onChange={this.onChangeSymbol}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="contexts">Контексты</label>
                        <AsyncSelect
                            isMulti
                            id='contexts-style'
                            loadOptions={getContexts}
                            defaultOptions
                            onChange={(contexts) => this.setState({contexts})}
                        />
                    </div>
                    {this.state.showForm
                        ?
                        <div className="form-group" id='add-context-form'>
                            <AsyncSelect
                                value={context_type}
                                loadOptions={getContextTypes}
                                defaultOptions
                                onChange={context_type => this.setState({context_type})}
                            />
                            <textarea
                                style={{fontSize: '14px'}}
                                value={context_description}
                                className="form-control"
                                rows="5"
                                name='context_description'
                                onChange={e => this.setState({context_description: e.target.value})}
                            />
                            <button id='cancel-adding-context' onClick={() => this.setState({showForm: false})}>
                                Отмена
                            </button>
                        </div>
                        :
                        <div>
                            <button 
                                id="add-context"
                                onClick={() => this.setState({showForm: true})}
                                title='Добавить новый контекст'
                            >+</button>
                        </div>

                    }
                </div>
                <div className="btn-group" role="group" id='btns-save'>
                    <button type='submit' onClick={this.onSubmit} style={{marginRight: '10px'}}>Сохранить</button>
                    <button onClick={this.onToggle}>Отмена</button>
                </div>
            </div>
        )
    }
}
