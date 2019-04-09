import React, {Component} from 'react';


export default class AddSymbolForm extends Component {

    render() {

        return(
            <div>
                <form>
                    <div className="form-group">
                        <label htmlFor="symbol">Символ</label>
                        <input
                            type="text"
                            className="form-control"
                            id="symbol"
                            style={{backgroundColor: '#fff', color: '#000'}}
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
                    <button>Сохранить</button>
                </form>
            </div>
        )
    }
}
