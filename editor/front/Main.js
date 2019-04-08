import React, {Component} from 'react';
import { SymbolNavigation, PageWindow, AddSymbolForm } from "./components"
import { Row, Col } from 'react-bootstrap';


class Main extends Component {
    render() {
        return(
            <div className='container'>
                <Row id='row-editor'>
                    <Col md={2} lg={2}>
                        <SymbolNavigation />
                    </Col>
                    <Col md={8} lg={8}>
                        <PageWindow />
                    </Col>
                    <Col md={2} lg={2}>
                        <AddSymbolForm />
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Main;
