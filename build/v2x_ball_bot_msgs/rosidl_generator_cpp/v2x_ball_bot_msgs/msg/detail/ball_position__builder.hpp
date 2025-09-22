// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallPosition.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_POSITION__BUILDER_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_POSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "v2x_ball_bot_msgs/msg/detail/ball_position__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace v2x_ball_bot_msgs
{

namespace msg
{

namespace builder
{

class Init_BallPosition_z
{
public:
  explicit Init_BallPosition_z(::v2x_ball_bot_msgs::msg::BallPosition & msg)
  : msg_(msg)
  {}
  ::v2x_ball_bot_msgs::msg::BallPosition z(::v2x_ball_bot_msgs::msg::BallPosition::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallPosition msg_;
};

class Init_BallPosition_y
{
public:
  explicit Init_BallPosition_y(::v2x_ball_bot_msgs::msg::BallPosition & msg)
  : msg_(msg)
  {}
  Init_BallPosition_z y(::v2x_ball_bot_msgs::msg::BallPosition::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_BallPosition_z(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallPosition msg_;
};

class Init_BallPosition_x
{
public:
  Init_BallPosition_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BallPosition_y x(::v2x_ball_bot_msgs::msg::BallPosition::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_BallPosition_y(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallPosition msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::v2x_ball_bot_msgs::msg::BallPosition>()
{
  return v2x_ball_bot_msgs::msg::builder::Init_BallPosition_x();
}

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_POSITION__BUILDER_HPP_
