import React, {Component} from 'react';
import Select from 'react-select';
import Creatable from 'react-select/lib/Creatable';


export default class AddSymbolForm extends Component  {

    constructor(props) {
        super(props);
        this.state = {
            context: this.getInitialContext()
        }
    }

    getInitialContext = () => {
        return {
            symbol: {descriptions: []},
            start: 0,
            word_shift: 0,
            word_len: 0,
            end: 0,
            text: '',
            description: ''
        }
    }

    onChangeSymbol = (e) => {
        let new_symbol = {
            value: e.__isNew__ ? 'new' : e.value, 
            label: e.label, 
            descriptions: e.__isNew__ ? [] : e.descriptions
        }
        let prevContext = this.state.context;
        let nextContext = {
            ...prevContext,
            symbol: new_symbol
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

    getLocation = (selected_text) => {
        const { text_chunk } = this.props;
        let word_shift = text_chunk.indexOf(selected_text);
        let word_len = selected_text.length;

        let start = 0;
        let end = text_chunk.length;
        let end_characters = ['.', '?', '!'];

        for (let i = word_shift; i > 0; i--) {
            if (end_characters.includes(text_chunk[i])) {
                start = i;
                break;
            }
        }

        // мы должны "захватывать" символ окончания предложения.
        // ниже мы обрабатываем ситуацию, когда предложение оканчивается, например, на ???
        let last_symbol = '';
        for (let i = word_shift + word_len; i < text_chunk.length; i++) {
            if (end_characters.includes(text_chunk[i])) {
                last_symbol = text_chunk;
            } else if (last_symbol) {
                end = i - 1;
                break;
            }
        }

        word_shift = word_shift - start;
        start = start + this.props.start_position;
        return {start, word_shift, word_len, end}
    }
    
    onToggle = () => {
        const { symbolAddition, toggleSymbolAddition } = this.props;
        let context = {}

        if (!symbolAddition) {
            let sel = window.getSelection();
            let selected_text = sel.toString()
            
            if (selected_text && sel.anchorNode && sel.anchorNode.parentElement.id == 'page-window'){
                let { start, word_shift, word_len, end } = this.getLocation(selected_text);
                                
                let new_context = {
                    ...this.state.context,
                    text: selected_text,
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
            this.setState({context: this.getInitialContext()})
        }
        toggleSymbolAddition();
    }

    onSubmit = (e) => {
        e.preventDefault();
        let {symbol, description} = this.state.context;
        if (!symbol.value) {
            alert('Выберите или добавьте новый символ!');
        } else if (symbol.value == 'new' && !description) {
            alert('При добавлении нового символа нужно обязательно указать его описание!');
        } else {
            this.setState({context: this.getInitialContext()});
            this.props.tmpSaveSymbol(this.state.context);
        }
    }

    render() {
        const {symbolAddition, symbols} = this.props;
        const {symbol} = this.state.context;

        if (!symbolAddition) {
            return <button onClick={this.onToggle}>Добавить символ</button>
        }

        return(
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
                {
                    symbol.descriptions.length > 0
                    ?
                    <div>
                        <label htmlFor='symbol-descriptions'>Значения символа</label>
                        <div id='symbol-descriptions'>
                        {
                            symbol.descriptions.map((d, i) => {
                                return <div key={i} title={d}>{i+1}) {d.slice(0, 50)}{d.length > 50 ? '...' : ''}</div>
                            })
                        }
                        </div>
                    </div>
                    :
                    null
                }
                <div className="form-group">
                    <label htmlFor="description">Новое значение символа</label>
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
