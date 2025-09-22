// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallArray.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"
// Member 'balls'
#include "v2x_ball_bot_msgs/msg/detail/ball__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__v2x_ball_bot_msgs__msg__BallArray __attribute__((deprecated))
#else
# define DEPRECATED__v2x_ball_bot_msgs__msg__BallArray __declspec(deprecated)
#endif

namespace v2x_ball_bot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BallArray_
{
  using Type = BallArray_<ContainerAllocator>;

  explicit BallArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    (void)_init;
  }

  explicit BallArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _balls_type =
    std::vector<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>>;
  _balls_type balls;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__balls(
    const std::vector<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>> & _arg)
  {
    this->balls = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__BallArray
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__BallArray
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BallArray_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->balls != other.balls) {
      return false;
    }
    return true;
  }
  bool operator!=(const BallArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BallArray_

// alias to use template instance with default allocator
using BallArray =
  v2x_ball_bot_msgs::msg::BallArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_HPP_
