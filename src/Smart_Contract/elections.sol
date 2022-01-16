pragma solidity >=0.8.0 <0.9.0;
pragma abicoder v2;

contract ElectionsContract {
    //Model a candidate
    struct Candidate {
        string name;
        string description;
        uint256 voteCount;
    }
    enum State {
        Created,
        Voting,
        Ended
    }
    // Model election
    struct Election {
        string name;
        // Store accounts which have voted
        mapping(string => bool) voters;
        mapping(uint256 => Candidate) candidates;
        State state;
        // Check if I have this ID
        // mapping(string => bool) candidatesIDs;
        // Store Candidate Count
        // string[] candidatesIDsArray;
        uint256 candidatesCount;
        uint256 totalVoteCount;
    }

    // Store Elections
    mapping(uint256 => Election) elections;
    // Store Election Count
    uint256 electionsCount;

    modifier validateElection(uint256 _electionID) {
        require(_electionID > 0 && _electionID <= electionsCount);
        _;
    }

    modifier inState(State _state, uint256 _electionID) {
        require(elections[_electionID].state == _state);
        _;
    }

    modifier validateCandidate(uint256 _electionID, uint256 _candidateID) {
        require(
            _candidateID > 0 &&
                _candidateID <= elections[_electionID].candidatesCount
        );
        _;
    }

    // // voted event
    // event votedEvent(uint256 indexed _candidateId);

    // Constructor
    // constructor() public {
    //     addCandidate("Candidate 1");
    //     addCandidate("Candidate 2");
    // }

    function createElection(string memory _name)
        public
        returns (uint256 electionID)
    {
        electionID = electionsCount++;
        elections[electionID].name = _name;
        elections[electionID].state = State.Created;
    }

    function createCandidate(
        uint256 _electionID,
        string memory _name,
        string memory _description
    )
        public
        validateElection(_electionID)
        inState(State.Created, _electionID)
        returns (uint256)
    {
        // create candidateID
        uint256 candidateID = elections[_electionID].candidatesCount++;
        elections[_electionID].candidates[candidateID] = Candidate(
            _name,
            _description,
            0
        );
        return candidateID;

        // elections[_electionID].candidatesIDs[candidateID] = true;
        // elections[_electionID].candidatesIDsArray.push(_candidateID);
    }

    function vote(
        uint256 _electionID,
        uint256 _candidateID,
        string memory _userID
    )
        public
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        inState(State.Voting, _electionID)
    {
        // require that address hasn't voted before
        if (!elections[_electionID].voters[_userID]) {
            elections[_electionID].voters[_userID] = true;
            elections[_electionID].totalVoteCount++;
            elections[_electionID].candidates[_candidateID].voteCount++;
        }

        // record that voter has voted

        // update candidate vote count

        // trigger vote event
        // emit votedEvent(_candidateId);
    }

    function startElection(uint256 _electionID)
        public
        inState(State.Created, _electionID)
        validateElection(_electionID)
    {
        elections[_electionID].state = State.Voting;
    }

    function endElection(uint256 _electionID)
        public
        validateElection(_electionID)
        inState(State.Voting, _electionID)
    {
        elections[_electionID].state = State.Ended;
    }

    function getElectionsCount() public view returns (uint256) {
        return electionsCount;
    }

    function getElectionName(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (string memory)
    {
        return elections[_electionID].name;
    }

    function getElectionVotes(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (uint256)
    {
        return elections[_electionID].totalVoteCount;
    }

    function getElectionCandidatesCount(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (uint256)
    {
        return elections[_electionID].candidatesCount;
    }

    function getCandidateName(uint256 _electionID, uint256 _candidateID)
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (string memory)
    {
        return elections[_electionID].candidates[_candidateID].name;
    }

    function getCandidateDescription(uint256 _electionID, uint256 _candidateID)
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (string memory)
    {
        return elections[_electionID].candidates[_candidateID].description;
    }

    function getCandidateVotes(uint256 _electionID, uint256 _candidateID)
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (uint256)
    {
        return elections[_electionID].candidates[_candidateID].voteCount;
    }

    function getElectionStatus(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (uint256)
    {
        State state = elections[_electionID].state;
        if (state == State.Created) return 0;
        if (state == State.Voting) return 1;
        if (state == State.Ended) return 2;
    }

    function hasUserVoted(uint256 _electionID, string memory _userID)
        public
        view
        returns (bool)
    {
        return elections[_electionID].voters[_userID];
    }

    // function getElectionCandidateIDs(uint256 _electionID)
    //     public
    //     view
    //     validateElection(_electionID)
    //     returns (string[] memory)
    // {
    //     return elections[_electionID].candidatesIDsArray;
    // }
}
