import React, {Component} from 'react';
import Select from 'react-select';


export default class AddSymbolForm extends Component  {

    constructor(props) {
        super(props);
        this.state = {
            context: this.getInitialContext()
        }
    }

    getInitialContext = () => {
        return {
            symbol: {},
            start: 0,
            word_shift: 0,
            word_len: 0,
            end: 0,
            text: '',
            description: ''
        }
    }

    onChangeSymbol = (e) => {
        let prevContext = this.state.context;
        let nextContext = {
            ...prevContext,
            symbol: e
        }
        this.setState({context: nextContext});
    }

    onChageContext(e) {
        let prevContext = this.state.context;
        let nextContext = {
            ...prevContext,
            description: e.target.value
        }
        this.setState({context: nextContext})
    }

    getLocation = (sel) => {
        const { text_chunk } = this.props;
        let word_shift = sel.anchorOffset;
        let word_len = sel.focusOffset - sel.anchorOffset;
        let start = 0;
        let end = text_chunk.length;

        for (let i = word_shift; i > 0; i--) {
            if (text_chunk[i] == '.') {
                start = i;
                break;
            }
        }
        for (let i = sel.focusOffset; i < text_chunk.length; i++) {
            if (text_chunk[i] == '.') {
                end = i;
                break
            }
        }
        return {start, word_shift, word_len, end}
    }
    
    onToggle = () => {
        const { symbolAddition, toggleSymbolAddition } = this.props;
        let context = {}

        if (!symbolAddition) {
            let sel = window.getSelection();
            let text = sel.toString()
            
            if (text && sel.anchorNode && sel.anchorNode.parentElement.id == 'page-window'){
                let { start, word_shift, word_len, end } = this.getLocation(sel);
                                
                let new_context = {
                    ...this.state.context,
                    text: text,
                    start: start,
                    word_shift: word_shift,
                    word_len: word_len,
                    end: end
                }
                this.setState({context: new_context});

            } else {
                alert('Прежде, чем добавить новый символ,\n' + 
                      'вы должны выделить текст на странице\n' +
                      'для определения контекста этого символа!');
                return
            }
        } else {
            this.setState({context: this.getInitialContext})
        }
        toggleSymbolAddition();
    }

    onSubmit = (e) => {
        e.preventDefault();
        this.props.tmpSaveSymbol(this.state.context);
    }

    render() {
        const {symbolAddition, symbols} = this.props;

        if (!symbolAddition) {
            return <button onClick={this.onToggle}>Добавить символ</button>
        }

        return(
            <div>

                    <div className="form-group">
                        <label htmlFor="symbol">Символ</label>
                        <Select
                            id='symbol'
                            value={this.state.context.symbol}
                            options={symbols}
                            onChange={this.onChangeSymbol}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="description">Описание символа</label>
                        <textarea
                            style={{fontSize: '14px'}}
                            value={this.state.context.description}
                            className="form-control"
                            rows="5"
                            name='description'
                            id="description"
                            onChange={::this.onChageContext}
                        />
                    </div>
                    <div className="btn-group" role="group">
                        <button type='submit' onClick={this.onSubmit} style={{marginRight: '10px'}}>Сохранить</button>
                        <button onClick={this.onToggle}>Отмена</button>
                    </div>
            </div>
        )
    }
}
