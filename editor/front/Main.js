import React, {Component} from 'react';
import { SymbolNavigation, PageWindow, AddSymbolForm } from "./components"
import { Row, Col } from 'react-bootstrap';


export default class Main extends Component {

    render() {

        return(
            <div className='container'>
                <Row id='row-editor'>
                    <Col md={2} lg={2}>
                        <SymbolNavigation/>
                    </Col>
                    <Col md={6} lg={6}>
                        <PageWindow/>
                    </Col>
                    <Col md={4} lg={4}>
                        <AddSymbolForm/>
                    </Col>
                </Row>
            </div>
        )
    }
}
