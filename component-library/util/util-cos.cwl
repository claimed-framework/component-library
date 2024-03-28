cwlVersion: v1.2
class: CommandLineTool

baseCommand: "claimed"

inputs:
  component:
    type: string
    default: docker.io/romeokienzler/claimed-util-cos:0.39
    inputBinding:
      position: 1
      prefix: --component
  log_level:
    type: string
    default: "INFO"
    inputBinding:
      position: 2
      prefix: --log_level
  cos_connection:
    type: string
    default: None
    inputBinding:
      position: 3
      prefix: --cos_connection
  local_path:
    type: string
    default: None
    inputBinding:
      position: 4
      prefix: --local_path
  recursive:
    type: bool
    default: False
    inputBinding:
      position: 5
      prefix: --recursive
  operation:
    type: string
    default: None
    inputBinding:
      position: 6
      prefix: --operation


outputs: []
