import React from 'react'

function Quote(props) {
  return (
    <div>
      <h1>{props.quoter}</h1>
      <p>{props.quote}</p>
    </div>
  )
}

export default Quote