
import React, {Component} from 'react';
import Select from 'react-select';


const AddSymbolForm = ({...props}) => {
    const {symbolAddition, toggleSymbolAddition, symbols} = props;

    if (!symbolAddition) {
        return <button onClick={toggleSymbolAddition}>Добавить символ</button>
    }

    return(
        <div>
            <form>
                <div className="form-group">
                    <label htmlFor="symbol">Символ</label>
                    <Select
                        id='symbol'
                        options={symbols}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Описание символа</label>
                    <textarea
                        style={{fontSize: '14px'}}
                        className="form-control"
                        rows="5"
                        id="description"
                    />
                </div>
                <div className="btn-group" role="group">
                    <button type='submit' style={{marginRight: '10px'}}>Сохранить</button>
                    <button onClick={toggleSymbolAddition}>Отмена</button>
                </div>
            </form>
        </div>
    )
}

export default AddSymbolForm
