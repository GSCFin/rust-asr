# Knowledge Graph: jito-solana

## Statistics
- **Nodes:** 15441
- **Edges:** 18930
- **Clusters:** 71

## Entity Types
- fn: 12267
- struct: 2254
- enum: 607
- impl: 169
- trait: 144

## Clusters (Layers)
### Application Layer
- AbsRequestHandlers
- AbsStatus
- AccountsBackgroundService
- AdminRpc
- AdminRpcContactInfo
- AdminRpcImpl
- AdminRpcRepairWhitelist
- AdminRpcRequestMetadata
- AggregateCommitmentService
- AlpenglowPortOverride
- ... and 700 more

### Domain Layer
- BenchSetup
- CostModel
- CostTracker
- CostTrackerError
- CostTrackerPostAnalysis
- LeaderSchedule
- SetIdentityArgs
- SharedBlockCost
- SystemProgramAccountAllocation
- TransactionCost
- ... and 110 more

### Infrastructure Layer
- AccessToken
- AccessTokenInner
- AccountAddressFilter
- AccountAddressRange
- AccountBlockFormat
- AccountForGeyser
- AccountForStorage
- AccountFromStorage
- AccountIndex
- AccountIndexWriterEntry
- ... and 1771 more

### Interface Layer
- BucketApi
- Default
- EpochRewardsPeriodActiveErrorData
- Error
- ErrorKind
- HttpSender
- MinContextSlotNotReachedErrorData
- NodeUnhealthyErrorData
- RpcBundleExecutionError
- RpcBundleRequest
- ... and 26 more

### Module: args
- RocksdbCompactionThreadsArg
- RocksdbFlushThreadsArg
- args
- default_json_rpc_config
- default_rpc_bigtable_config
- test_default_bigtable_app_profile_id_unchanged
- test_default_bigtable_instance_name_unchanged
- test_default_bigtable_max_message_size_unchanged
- test_default_bigtable_timeout_unchanged
- test_default_health_check_slot_distance_unchanged
- ... and 74 more

### Module: authorized_voter
- AuthorizedVoterAddArgs
- verify_args_struct_by_command_authorized_voter_add_default
- verify_args_struct_by_command_authorized_voter_add_with_authorized_voter_keypair

### Module: bam
- BamUrlError
- argument
- assert_eq_extract_bam_url
- assert_extract_bam_url_error
- create_test_matches
- extract_bam_url
- normalize_bam_url
- test_extract_bam_url_empty_inputs
- test_extract_bam_url_invalid_formats
- test_extract_bam_url_invalid_ipv6_address
- ... and 5 more

### Module: bank
- AcceptableScanResults
- AccountsDetails
- BankAbiTestWrapper
- BankHashComponents
- BankHashDetails
- CacheValue
- DepositFeeError
- Features
- FeeDistribution
- FreezeBank1
- ... and 315 more

### Module: banking_stage
- BankingPacketReceivers
- BufferedPacketsDecision
- CommitTransactionDetails
- CommittedTransactionsCounts
- Committer
- ConsumeBufferedPacketsTimings
- ConsumeWork
- ConsumeWorker
- ConsumeWorkerCountMetrics
- ConsumeWorkerError
- ... and 222 more

### Module: batched_grouped_ciphertext_validity
- BatchedGroupedCiphertext2HandlesValidityProofContext
- BatchedGroupedCiphertext2HandlesValidityProofData
- BatchedGroupedCiphertext3HandlesValidityProofContext
- BatchedGroupedCiphertext3HandlesValidityProofData
- test_ciphertext_validity_proof_instruction_correctness

### Module: batched_grouped_ciphertext_validity_proof
- BatchedGroupedCiphertext2HandlesValidityProof
- BatchedGroupedCiphertext3HandlesValidityProof
- test_batched_grouped_ciphertext_validity_proof

### Module: batched_range_proof
- BatchedRangeProofContext
- BatchedRangeProofU128Data
- BatchedRangeProofU256Data
- BatchedRangeProofU64Data
- TryInto
- test_batched_range_proof_256_instruction_correctness
- test_batched_range_proof_u128_instruction_correctness
- test_batched_range_proof_u64_instruction_correctness
- try_into

### Module: benches
- Bench
- BenchAuthorize
- BenchAuthorizeChecked
- BenchAuthorizeCheckedWithSeed
- BenchAuthorizeWithSeed
- BenchCompactUpdateVoteState
- BenchEnv
- BenchFrame
- BenchInitializeAccount
- BenchTowerSync
- ... and 319 more

### Module: bin
- Cli
- agave_xdp
- drop_frags
- exec
- has_frags
- press_enter
- remove_directory_contents

### Module: block_creation_loop
- LoopMetrics
- SlotMetrics

### Module: blockstore
- AddressSignatures
- BankHash
- BlockHeight
- BlockstoreError
- Blocktime
- ColumnIndexDeprecation
- ColumnName
- DeadSlots
- DuplicateSlots
- IndexError
- ... and 43 more

### Module: broadcast_stage
- BatchCounter
- BroadcastDuplicatesConfig
- BroadcastDuplicatesRun
- BroadcastError
- BroadcastFakeShredsRun
- BroadcastShredBatchInfo
- BroadcastStats
- ClusterPartition
- FailEntryVerificationBroadcastRun
- InsertShredsStats
- ... and 24 more

### Module: bundle_stage
- BundleAccountLocker
- BundleAccountLockerError
- BundleAccountLocks
- BundleConsumer
- BundlePacketDeserializer
- BundleStageLeaderMetrics
- BundleStageStats
- BundleStageStatsMetricsTracker
- account_locks
- bundle_stage_metrics_tracker
- ... and 30 more

### Module: cli
- AccountsDbBackgroundThreadsArg
- AccountsDbForegroundThreadsArg
- AccountsIndexFlushThreadsArg
- BlockProductionNumWorkersArg
- DefaultThreadArgs
- IpEchoServerThreadsArg
- NumThreadConfig
- RayonGlobalThreadsArg
- ReplayForksThreadsArg
- ReplayTransactionsThreadsArg
- ... and 12 more

### Module: commands
- BumpLevel
- CommandArgs
- FromClapArgMatches
- bump_version
- from_clap_arg_match
- test_bump_version
- verify_args_struct_by_command
- verify_args_struct_by_command_is_error

### Module: consensus
- AncestorIterator
- CandidateVoteAndResetBanks
- ForkChoice
- ForkInfo
- ForkProgress
- ForkStats
- GetSlotHash
- HeaviestSubtreeForkChoice
- LatestValidatorVotesForFrozenBanks
- LockoutInterval
- ... and 162 more

### Module: consensus_pool
- AggregateError
- BlockProductionParent
- BuildError
- BuilderType
- CertificateBuilder
- CertificateStats
- ConsensusPoolStats
- InternalVotePool
- ParentReadyStatus
- ParentReadyTracker
- ... and 38 more

### Module: contact_info
- ContactInfoArgs
- verify_args_struct_by_command_contact_info_output_default
- verify_args_struct_by_command_contact_info_output_invalid
- verify_args_struct_by_command_contact_info_output_json
- verify_args_struct_by_command_contact_info_output_json_compact

### Module: core_bpf_migration
- CoreBpfMigrationError
- SourceBuffer
- TargetBpfV2
- TargetBuiltin
- TargetCoreBpf
- TestContext
- TestPrototype
- activate_feature_and_run_checks
- calculate_post_migration_capitalization_and_accounts_data_size_delta_off_chain
- calculate_post_upgrade_capitalization_and_accounts_data_size_delta_off_chain
- ... and 39 more

### Module: encryption
- AeCiphertext
- AeKey
- AuthenticatedEncryption
- ConstantTimeEq
- DecodePrecomputation
- DecryptHandle
- DiscreteLog
- DiscreteLogError
- ElGamal
- ElGamalCiphertext
- ... and 77 more

### Module: examples
- Regime
- Results
- default_num_tpu_transaction_forward_receive_threads
- load_staked_nodes_overrides
- make_config_dedicated
- make_config_shared
- parse_duration

### Module: exit
- ExitArgs
- PostExitAction
- poll_until_pid_terminates
- verify_args_struct_by_command_exit_default
- verify_args_struct_by_command_exit_with_force
- verify_args_struct_by_command_exit_with_max_delinquent_stake
- verify_args_struct_by_command_exit_with_min_idle_time
- verify_args_struct_by_command_exit_with_post_exit_action
- verify_args_struct_by_command_exit_with_skip_health_check
- verify_args_struct_by_command_exit_with_skip_new_snapshot_check

### Module: extension
- check_no_panic
- parse_confidential_mint_burn_instruction
- parse_confidential_transfer_fee_instruction
- parse_confidential_transfer_instruction
- parse_cpi_guard_instruction
- parse_default_account_state_instruction
- parse_group_member_pointer_instruction
- parse_group_pointer_instruction
- parse_initialize_mint_close_authority_instruction
- parse_initialize_permanent_delegate_instruction
- ... and 36 more

### Module: fixture
- FixtureError
- InstrContext
- InstrEffects
- feature_u64

### Module: forwarding_stage
- PacketContainer
- PacketContainerEntry
- min_priority
- pop_max
- pop_min
- simple_packet_with_flags
- test_packet_container_pop_max
- test_packet_container_pop_min
- test_packet_container_status

### Module: grouped_ciphertext_validity
- GroupedCiphertext2HandlesValidityProofContext
- GroupedCiphertext2HandlesValidityProofData
- GroupedCiphertext3HandlesValidityProofContext
- GroupedCiphertext3HandlesValidityProofData

### Module: grouped_ciphertext_validity_proof
- GroupedCiphertext2HandlesValidityProof
- GroupedCiphertext3HandlesValidityProof
- test_grouped_ciphertext_3_handles_validity_proof_correctness
- test_grouped_ciphertext_3_handles_validity_proof_edge_cases
- test_grouped_ciphertext_validity_proof_correctness
- test_grouped_ciphertext_validity_proof_edge_cases

### Module: inflation_rewards
- CalculatedStakePoints
- CalculatedStakeRewards
- InflationPointCalculationEvent
- PointValue
- SkippedReason
- calculate_points
- calculate_rewards_tests
- calculate_stake_points
- calculate_stake_points_and_credits
- calculate_stake_rewards
- ... and 8 more

### Module: install
- main

### Module: instruction
- CiphertextCiphertextEqualityProofContext
- CiphertextCiphertextEqualityProofData
- CiphertextCommitmentEqualityProofContext
- CiphertextCommitmentEqualityProofData
- FeeSigmaProofContext
- FeeSigmaProofData
- InstructionError
- ProofType
- PubkeyValidityData
- PubkeyValidityProofContext
- ... and 18 more

### Module: io_uring
- AllocError
- AsMut
- CloseOp
- Directory
- FileCreatorOp
- FileCreatorState
- FileCreatorStats
- FixedIoBuffer
- IoUringFileCreator
- LargeBuffer
- ... and 47 more

### Module: leader_schedule
- SlotLeaderInfo
- test_get_vote_key_at_slot_index
- test_index

### Module: manage_block_production
- ManageBlockProductionArgs
- verify_args_struct_by_command_manage_block_production_default
- verify_args_struct_by_command_manage_block_production_with_args
- verify_args_struct_by_command_manage_block_production_with_args_pacing_disabled

### Module: monitor
- monitor_validator

### Module: nonblocking
- ClientConnectionTracker
- ConnectionContext
- ConnectionEntry
- ConnectionHandlerError
- ConnectionPeerType
- ConnectionRateLimiter
- ConnectionStreamCounter
- ConnectionTable
- ConnectionTableKey
- ConnectionTableType
- ... and 157 more

### Module: partitioned_epoch_rewards
- CalculateValidatorRewardsResult
- DelegationRewards
- DistributionError
- DistributionResults
- EpochRewardCalculateParamInfo
- EpochRewardPhase
- EpochRewardStatus
- FilteredStakeDelegations
- KeyedRewardsAndNumPartitions
- PartitionedRewardsCalculation
- ... and 102 more

### Module: plugin
- PluginLoadArgs
- PluginReloadArgs
- PluginUnloadArgs
- verify_args_struct_by_command_plugin_load_default
- verify_args_struct_by_command_plugin_load_with_config
- verify_args_struct_by_command_plugin_reload_default
- verify_args_struct_by_command_plugin_reload_with_name
- verify_args_struct_by_command_plugin_reload_with_name_and_config
- verify_args_struct_by_command_plugin_unload_default
- verify_args_struct_by_command_plugin_unload_with_name

### Module: pod
- CompressedRistretto
- GroupedElGamalCiphertext2Handles
- GroupedElGamalCiphertext3Handles
- PodProofType
- PodU16
- PodU64
- RangeProofU128
- RangeProofU256
- RangeProofU64
- ae_ciphertext_fromstr
- ... and 7 more

### Module: proxy
- AuthInterceptor
- BlockBuilderFeeInfo
- BlockEngineConfig
- BlockEngineStage
- BlockEngineStageStats
- FetchStageManager
- FetchStageState
- Interceptor
- PingError
- ProxyError
- ... and 30 more

### Module: quic_networking
- IoErrorWithPartialEq

### Module: range_proof
- BulletproofGens
- G
- GeneratorsChain
- GensIter
- H
- InnerProductProof
- RangeProof
- RangeProofGenerationError
- RangeProofGeneratorError
- RangeProofVerificationError
- ... and 9 more

### Module: repair
- AncestorDuplicateSlotToRepair
- AncestorHashesRepairType
- AncestorHashesResponse
- AncestorRequestDecision
- AncestorRequestStatus
- AncestorRequestType
- BankFrozenState
- BankStatus
- ClusterConfirmedHash
- DeadState
- ... and 220 more

### Module: repair_shred_from_peer
- RepairShredFromPeerArgs
- verify_args_struct_by_command_repair_shred_from_peer_missing_pubkey
- verify_args_struct_by_command_repair_shred_from_peer_missing_slot_and_shred
- verify_args_struct_by_command_repair_shred_from_peer_with_pubkey

### Module: repair_whitelist
- RepairWhitelistGetArgs
- RepairWhitelistSetArgs
- verify_args_struct_by_command_repair_whitelist_get_default
- verify_args_struct_by_command_repair_whitelist_get_with_output
- verify_args_struct_by_command_repair_whitelist_set_with_multiple_whitelist
- verify_args_struct_by_command_repair_whitelist_set_with_single_whitelist

### Module: rpc
- get_account_from_overwrites_or_bank

### Module: run
- Operation
- RunArgs
- add_args
- new_snapshot_config
- parse_banking_trace_dir_byte_limit
- tip_manager_config_from_matches
- validators_set
- verify_args_struct_by_command_run_is_error_with_identity_setup
- verify_args_struct_by_command_run_with_allow_private_addr
- verify_args_struct_by_command_run_with_entrypoints
- ... and 6 more

### Module: runtime_transaction
- TestTransaction
- add_compute_unit_limit
- add_compute_unit_price
- add_loaded_accounts_bytes
- assert_translation
- from_sanitized_transaction_view
- from_transaction_for_tests
- get_is_simple_vote
- load_dynamic_metadata
- non_vote_sanitized_versioned_transaction
- ... and 8 more

### Module: serde_snapshot
- SerdeAccountsLtHash
- SerdeInstructionError
- SerdeObsoleteAccounts
- SerdeObsoleteAccountsMap
- SerdeTransactionError
- accountsdb_from_stream
- accountsdb_to_stream
- check_accounts_local
- context_accountsdb_from_stream
- copy_append_vecs
- ... and 20 more

### Module: set_log_filter
- SetLogFilterArgs
- verify_args_struct_by_command_set_log_filter_default
- verify_args_struct_by_command_set_log_filter_with_filter

### Module: set_public_address
- SetPublicAddressArgs
- verify_args_struct_by_command_set_public_address_tpu
- verify_args_struct_by_command_set_public_address_tpu_and_tpu_forwards
- verify_args_struct_by_command_set_public_address_tpu_forwards
- verify_args_struct_by_command_set_public_default

### Module: shred
- Payload
- PayloadMutGuard
- ProcessShredsStats
- ShredCodeTrait
- ShredDataTrait
- ShredFetchStats
- ShredTrait
- chained_merkle_root_offset
- cmp_shred_erasure_shard_index
- coding_header
- ... and 88 more

### Module: sigma_proofs
- CiphertextCiphertextEqualityProof
- CiphertextCommitmentEqualityProof
- ConditionallySelectable
- EqualityProofVerificationError
- FeeEqualityProof
- FeeMaxProof
- FeeSigmaProof
- FeeSigmaProofVerificationError
- PubkeyValidityProof
- PubkeyValidityProofVerificationError
- ... and 19 more

### Module: snapshot_package
- are_snapshot_archive_kinds_the_same_kind
- are_snapshot_kinds_the_same_kind
- are_snapshot_packages_the_same_kind
- cmp_snapshot_archive_kinds_by_priority
- cmp_snapshot_kinds_by_priority
- cmp_snapshot_packages_by_priority
- test_are_snapshot_kinds_the_same_kind
- test_are_snapshot_packages_the_same_kind
- test_cmp_snapshot_archive_kinds_by_priority
- test_cmp_snapshot_kinds_by_priority
- ... and 1 more

### Module: src
- AbiExample
- AbortCase
- AccessType
- Account
- AccountAdditionalDataV3
- AccountData
- AccountFileFormat
- AccountKeyType
- AccountLoader
- AccountOverrides
- ... and 8383 more

### Module: staked_nodes_overrides
- StakedNodesOverridesArgs
- verify_args_struct_by_command_staked_nodes_overrides_default
- verify_args_struct_by_command_staked_nodes_overrides_path

### Module: stakes
- DeserializableDummy
- SerdeStakeAccountMapToDelegationFormat
- SerdeStakeAccountMapToStakeFormat
- SerdeStakeAccountsToDelegationFormat
- SerdeStakeAccountsToStakeFormat
- SerdeStakesToStakeFormat
- SerializableDummy
- serialize_stake_accounts_to_delegation_format
- serialize_stake_accounts_to_stake_format
- test_serde_stakes_to_delegation_format
- ... and 1 more

### Module: tests
- AbortReason
- BamNodeApi
- BaseSlot
- CheckTxData
- ClusterMode
- ExecutionStatus
- Fork
- ForkGraph
- InputData
- Inspect
- ... and 568 more

### Module: timer_manager
- TimerManagerStats
- TimerState
- Timers
- incr_timeout_count_with_heap_size
- max_heap_size
- next_fire
- progress
- set_timeout_count
- set_timeout_succeed_count
- timer_state_machine
- ... and 1 more

### Module: tip_manager
- ChangeBlockBuilderInstruction
- ChangeTipReceiverInstruction
- InitBumps
- InitializeTipDistributionAccountInstruction
- InitializeTipDistributionConfigInstruction
- InitializeTipPaymentInstruction
- JitoTipDistributionConfig
- JitoTipPaymentConfig
- JitoTipPaymentInitBumps
- TipDistributionAccount
- ... and 15 more

### Module: transaction_scheduler
- BamReceiveAndBuffer
- BamReceiveAndBufferMetrics
- BamScheduler
- BatchEntry
- BatchIdGenerator
- BatchIdOrTransactionState
- BatchInfo
- CostPacer
- DisconnectedError
- GreedyScheduler
- ... and 194 more

### Module: transfer
- FeeEncryption
- FeeParameters
- Role
- TransferAmountCiphertext
- TransferData
- TransferProof
- TransferProofContext
- TransferPubkeys
- TransferWithFeeData
- TransferWithFeeProof
- ... and 30 more

### Module: vote_state
- PreserveBehaviorInHandlerHelper
- authorize
- build_slot_hashes
- build_vote_state
- check_and_filter_proposed_vote_state
- check_lockouts
- check_slots_are_valid
- conflicting
- create_account_with_authorized
- create_v4_account_with_authorized
- ... and 78 more

### Module: vote_state_view
- AuthorizedVoterItem
- AuthorizedVotersListFrame
- BlsPubkeyCompressedFrame
- BlsPubkeyCompressedView
- CommissionFrame
- CommissionView
- EpochCreditsItem
- EpochCreditsListFrame
- LandedVoteItem
- LandedVotesListFrame
- ... and 54 more

### Module: wait_for_restart_window
- WaitForRestartWindowArgs
- command
- verify_args_struct_by_command_wait_for_restart_window_default
- verify_args_struct_by_command_wait_for_restart_window_identity
- verify_args_struct_by_command_wait_for_restart_window_max_delinquent_stake
- verify_args_struct_by_command_wait_for_restart_window_min_idle_time
- verify_args_struct_by_command_wait_for_restart_window_skip_health_check
- verify_args_struct_by_command_wait_for_restart_window_skip_new_snapshot_check
- wait_for_restart_window

### Module: zk_token_elgamal
- add_with_lo_hi
- pod
- subtract_from
- subtract_with_lo_hi
- test_add_to
- test_pod_decryption
- test_pod_range_proof_128
- test_pod_range_proof_64
- test_subtract_from
- test_transfer_arithmetic
- ... and 2 more

### Utilities
- AccountLocks
- AccountReadLocks
- AccountWriteLocks
- AgaveHandshakeError
- AgaveSession
- AgaveTpuToPackSession
- AgaveWorkerSession
- Amount
- ArgConstant
- ArgsConfig
- ... and 799 more


## Key Relationships
- references: 9960 connections
- derives: 4309 connections
- contains: 1959 connections
- implements: 1488 connections
- uses: 1214 connections