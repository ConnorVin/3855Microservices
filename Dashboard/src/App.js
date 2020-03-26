import React, {useState, useEffect} from 'react'
import Quote from "./Quote";
import axios from 'axios'


function Kanye() {
  const [athletes, setAthletes] = useState('athlete')
  const [races, setRaces] = useState('race')
  const [newAthlete, setNewAthlete] = useState('newAthlete')
  const [newRace, setNewRace] = useState('newRace')

  // Get the amount of Athletes
  const getNumAthletes = () => {
    axios.get('http://localhost:8090/report/athlete?startDate=2020-02-01T11:55&endDate=2020-04-20T11:55')
      .then(json => {
        // console.log(json.data.quote)
        console.log(json.data.length)
        setAthletes(json.data.length)
        // document.title = json.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  useEffect(() => {
    setInterval(getNumAthletes, 2000)
  }, [athletes])

  // Get the number of Races
  const getNumRaces = () => {
    axios.get('http://localhost:8090/report/race?startDate=2020-02-01T11:55&endDate=2020-04-20T11:55')
      .then(json => {
        // console.log(json.data.quote)
        console.log(json.data.length)
        setRaces(json.data.length)
        // document.title = json.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  useEffect(() => {
    setInterval(getNumRaces, 2000)
  }, [races])

  // Get the newest Athlete
  const getNewAthlete = () => {
    axios.get('http://localhost:8120/log/athlete')
      .then(json => {
        // console.log(json.data.quote)
        console.log(json.data.payload)
        setNewAthlete(json.data.payload.first_name)
        // document.title = json.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  useEffect(() => {
    setInterval(getNewAthlete, 2000)
  }, [newAthlete])

  // Get newest race
  const getNewRace = () => {
    axios.get('http://localhost:8120/log/race?offset=-1')
      .then(json => {
        // console.log(json.data.quote)
        console.log(json.data.payload)
        setNewRace(json.data.payload.race_id)
        // document.title = json.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  useEffect(() => {
    setInterval(getNewRace, 2000)
  }, [newRace])

  return (
    <div>
      <img src="https://i.pinimg.com/474x/3c/25/18/3c25183d9e074c314ada832d7d01845a--trophy-design-swim-team.jpg"/>
    <Quote quote={athletes} quoter={"Number of Athletes"} />
    <Quote quote={races} quoter={"Number of Races"} />
    <Quote quote={newAthlete} quoter={"Newest Athlete"} />
    <Quote quote={newRace} quoter={"Newest Race"} />
    <Quote quote={Date()} quoter={"Last Updated"} />
    </div>
  )
}

export default Kanye