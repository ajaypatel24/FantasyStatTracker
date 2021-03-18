
import React from 'react'
import {  Card, CardGroup, Button, Table, ButtonGroup } from 'react-bootstrap'
import axios from 'axios'

export default class StatTable extends React.Component {
    constructor(props) {
        super(props);

        this.state = {

            p: "",
            dataArray: [],
            Players: [],
            Categories: [],
            AllData: [],
            Leaders: [],
            f: [],
            show: false,
            Winning: [],
            showWinning: false,
            LeaderPlayer: [],
            Available: false

        };


        this.test = this.test.bind(this)
        this.getLeaders = this.getLeaders.bind(this)
        this.computeLeaders = this.computeLeaders.bind(this)
        this.winningMatchup = this.winningMatchup.bind(this)
    }


    async computeLeaders() {
        var bodyFormData = new FormData();
        bodyFormData.append("data", JSON.stringify(this.state.AllData))
        console.log(this.state.AllData)
        await axios.post('/win-calculator', bodyFormData)

            .then((response) => {
                console.log(response.data)
                this.setState({ Leaders: JSON.stringify(response.data) })
            })

        var obj = JSON.parse(this.state.Leaders)
        var catArr = []
        var cat = Object.keys(obj)

        for (var i in cat) {
            var entry = {}
            console.log(cat[i])
            entry[cat[i]] = [obj[cat[i]][0], obj[cat[i]][1]]
            console.log(entry[cat[i]])
            catArr.push(entry)
        }


        await this.setState({ f: catArr })
        console.log(catArr)
        console.log(this.state.f)

        {
            this.state.Categories.map((item, i) => {
                console.log(catArr[i][item][1])
                console.log(catArr[i][item][0])
            })
        }

        this.setState({ show: true })

    }

    test() {

        var arr = []
        var obj = JSON.parse(this.state.p)
        var g = Object.keys(obj)
        console.log(g)

        var catArray = []

        for (var i in g) {
            var w = {}
            w[g[i]] = obj[g[i]]
            arr.push(w)
        }

        console.log(arr)
        this.setState({ AllData: arr })
        for (var x in (arr[0][g[0]])) {
            catArray.push(x)
        }
        console.log(catArray)
        this.setState({ Players: g })
        this.setState({ dataArray: arr })
        this.setState({ Categories: catArray })

        {
            arr.map((item, i) => {
                console.log(g[i])
                console.log(item[g[i]].AST)

            })
        }

        this.setState({Available: true})



    }

    async componentDidMount() {

        await axios.get('/test')
            .then(response => {
                this.setState({ p: JSON.stringify(response.data) })
            })

        console.log(this.state.p)

    }

    async getLeaders() {
        var bodyFormData = new FormData();
        bodyFormData.append("data", JSON.stringify(this.state.AllData))
        console.log(this.state.AllData)
        await axios.post('/win-calculator', bodyFormData)

            .then((response) => {
                console.log(response.data)
                this.setState({ Leaders: JSON.stringify(response.data) })
            })



    }

    async winningMatchup() {
        var bodyFormData = new FormData();
        bodyFormData.append("data", JSON.stringify(this.state.AllData))
        console.log(this.state.AllData)
        await axios.post('/winning-matchups', bodyFormData)

            .then((response) => {
                console.log(response.data)
                this.setState({ Winning: JSON.stringify(response.data) })
            })


        var arr = []
        var obj = JSON.parse(this.state.Winning)
        var g = Object.keys(obj)

        for (var i in g) {
            var x = {}
            x[g[i]] = obj[g[i]]
            arr.push(x)
        }

        await this.setState({ Winning: arr })
        await this.setState({ LeaderPlayer: g })
        this.setState({ showWinning: true })

        console.log(this.state.Winning)

    }


    render() {


        return (


            <div>


                <Button onClick={this.test}>View Updated Current Week Stats and Leaders</Button>
                <CardGroup>
                    {this.state.dataArray.map((item, i) => {
                        return (
                            <Card style={{ width: '18rem' }}>
                                <Card.Body>

                                    <Card.Title
                                        adjustsFrontSizeToFit
                                        style={{ textAlign: 'center', fontSize: '1rem' }}>
                                        {this.state.Players[i]}
                                    </Card.Title>
                                    <Card.Text
                                        adjustsFrontSizeToFit
                                        style={{ textAlign: 'center', fontSize: '1rem' }}>
                                        <Table responsive size="sm">

                                            <tbody>
                                                {this.state.Categories.map((cat, x) =>
                                                    <tr>
                                                        <td>
                                                            {cat}
                                                        </td>

                                                        <td>
                                                            {item[this.state.Players[i]][cat]}
                                                        </td>

                                                    </tr>
                                                )}
                                            </tbody>
                                        </Table>
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                        )


                    })
                    }
                </CardGroup>

                {
                    this.state.Available === false ?
                    <p></p>
                    :
                    <ButtonGroup>
                    <Button onClick={this.computeLeaders}>Week Category Leaders</Button>
                    <Button onClick={this.winningMatchup}>Show that Aaron is Winner</Button>
                    </ButtonGroup>
                }
                



                {
                    this.state.show === false ?

                        <p></p>

                        :

                        <div>
                            <CardGroup>
                                {this.state.Categories.map((item, i) => {
                                    return (
                                        <Card>
                                            <Table>
                                                <div>
                                                    <thead>
                                                        <tr>
                                                            <p>{item}</p>
                                                        </tr>
                                                    </thead>
                                                    <tbody>

                                                        <td>{this.state.f[i][item][1]}</td>
                                                        <td>{this.state.f[i][item][0]}</td>
                                                    </tbody>
                                                </div>
                                            </Table>
                                        </Card>
                                    )
                                })}
                            </CardGroup>

                        </div>

                }


                {
                    this.state.showWinning === false ?
                        <p></p>

                        :

                        <div>

                            <Table>
                                {this.state.Winning.map((item, i) => {
                                    return (
                                        <div>

                                            <thead>
                                                <tr>{this.state.LeaderPlayer[i]} : {item[this.state.LeaderPlayer[i]].length} Teams</tr>
                                            </thead>
                                            <tbody>
                                            {item[this.state.LeaderPlayer[i]].length === 0 ? <th><strong>LOL</strong></th> : null}
                                                <tr>
                                                    
                                                    
                                                    {item[this.state.LeaderPlayer[i]].map((x, e) => {
                                                        return (<th>{x}</th>)
                                                        
                                                        
                                                    })
                                                    }
                                                
                                                
                                                </tr>
                                            </tbody>

                                        </div>

                                    )
                                })}
                            </Table>

                        </div>


                }







            </div>



        );
    };
}

