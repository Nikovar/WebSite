import React, {Component} from 'react';
import Select from 'react-select';
import {connect} from 'react-redux';
import {selectSymbol} from '../actions'


class SymbolNavigation extends Component {

    constructor(props) {
        super(props);
        this.state = {
            symbol: this.props.symbols[0]            
        };
    }

    
    onSelectSymbol = (symbol) => {
        this.setState({symbol})
    }    

    render() {
        console.log('existences', this.props.existences)
        console.log(this.props.existences[this.state.symbol.value])
        console.log('symbol', this.state.symbol)

        return(
            <div>
                <Select
                    value={this.state.symbol}
                    onChange={this.onSelectSymbol}
                    options={this.props.symbols}
                />
                <div id='symbol-navigation'>
                    {this.props.page} from  d{this.props.number_pages}
                </div>
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
        existences: state.editor.existences,
        symbols: state.editor.symbols,
        symbol: state.editor.symbol
    }
}

const mapDispatchToProps = dispatch => {
    return {
        selectSymbol: (symbol) => dispatch(selectSymbol)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(SymbolNavigation);
